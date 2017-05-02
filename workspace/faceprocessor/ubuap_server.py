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
import events
from sklearn import preprocessing

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
    users_processed = posts.find( {'interests_vector': { '$exists': True}, 'face_features': { '$exists': True}, 'city' : { '$exists': True}} ).sort( [ (u"active_search_score", -1),])

    def get_similarity_score(vec1, vec2):
        t = np.array(vec1) - np.array(vec2)
        try:
            tmp = float(np.dot(t, t.T))
        except Exception as e:
            print e
            return 1.0
        return tmp

    users_output = []
    searcher_interests_vector = events.prepare_vector(user_id)
    for user in users_processed:
        face_features_saved = json.loads(user['face_features'])
        interests_score_saved = json.loads(user[u'interests_vector'])
        score = get_similarity_score(mean_ideal_face, face_features_saved)
        interets_score_two = get_similarity_score(searcher_interests_vector, interests_score_saved)
        #user_id = user[u'uid']
        #print user_id
        #try:
        #    with open (u"/var/vk-data/{}/profile-{}.json".format(str(user_id)[-3:], user_id)) as f:
        #        user_photo = json.load(f)[u'basic'][u"photo_max"]
        #except:
        #    pass
        user_dict = {
            'uid': user[u'uid'],
            'photo': user['photo_url'],
            'vk_url': 'https://vk.com/id{}'.format(user[u'uid']),
            'age': user[u'age'] if user[u'age'] != -1 else -1,
            'city': user[u'city'][u'title'] if user[u'city'] != -1 else -1,
            'photo_score': score,
            'active_search_score': user[u'active_search_score'],
            'interests_score': interets_score_two,
        }
        users_output.append(user_dict)
    newlist = sorted(users_output, key=lambda k: k['photo_score']) 
    #    print i['photo_score'], 'http://vk.com/id{}'.format(i['uid'])    
    return json.dumps(newlist[:100])

if __name__ == "__main__":
    faceprocessor = FaceProcessor()
    app.run(host='0.0.0.0')


