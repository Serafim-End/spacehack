#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_cors import CORS, cross_origin
from flask import Flask, request
app = Flask(__name__)
CORS(app)
import numpy as np
import json
from faceprocessor import FaceProcessor
import os
from pymongo import MongoClient
import wget

def wget_photo(photo_url, output_directory='/var/vk-data/photos'):
    filename = photo_url.split('/')[-1]
    if not os.path.exists('{}/{}'.format(output_directory, filename)):
        target_file_path = wget.download(photo_url, out=output_directory)
    else:
        target_file_path = output_directory + '/' + filename
    return target_file_path


@app.route("/victims/", methods=['POST'])
def victims():
    income_json = request.json
    print income_json
    user_id = income_json["id"]
    photo_examples = income_json["urls"]
    face_features_list = []
    for photo in photo_examples:
        try:
            _path = wget_photo(photo)
            face_features = faceprocessor.get(_path)
            face_features_list.append(face_features)
        except Exception as e:
            print e
    mean_ideal_face = np.mean(np.stack(face_features_list), axis=0)
    client = MongoClient('localhost', 27017)
    db = client['users_and_features']
    posts = db.posts
    users_processed = list(posts.find( {'face_features' : { '$exists': True}} ))

    def get_similarity_score(vec1, vec2):
        t = np.array(vec1) - np.array(vec2)
        return np.dot(t, t)

    users_output = []
    for user in users_processed:
        face_features_saved = json.loads(user['face_features'])
        score = get_similarity_score(mean_ideal_face, face_features_saved)
        #user_id = user[u'uid']
        #print user_id
        #user_photo = 'https://vk.com/images/camera_400.png'
        #try:
        #    with open (u"/var/vk-data/{}/profile-{}.json".format(str(user_id)[-3:], user_id)) as f:
        #        user_photo = json.load(f)[u'basic'][u"photo_max"]
        #except:
        #    pass
        user_dict = {
            'uid': user[u'uid'],
            #'photo': user_photo,
            'vk_url': 'https://vk.com/id{}'.format(user[u'uid']),
            'age': 'no data',
            'city': 'no data',
            'photo_score': score,
            'active_search_score': 0,
            'interests_score': 0,
        }
        users_output.append(user_dict)
    newlist = sorted(users_output, key=lambda k: k['photo_score']) 
    #    print i['photo_score'], 'http://vk.com/id{}'.format(i['uid'])    
    return json.dumps(newlist[:100])

if __name__ == "__main__":
    faceprocessor = FaceProcessor()
    app.run(host='0.0.0.0')


