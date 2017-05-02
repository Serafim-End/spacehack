#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os.path
from faceprocessor import FaceProcessor
from pymongo import MongoClient
import openface
import os
import wget

client = MongoClient('localhost', 27017)
db = client['users_and_features']
posts = db.posts
faceprocessor = FaceProcessor()

ient = MongoClient('localhost', 27017)
db = client['users_and_features']
posts = db.posts
faceprocessor = FaceProcessor()
from random import shuffle

def wget_photo(photo_url, output_directory='/var/vk-data/photos'):
    filename = photo_url.split('/')[-1]
    if not os.path.exists('{}/{}'.format(output_directory, filename)):
        target_file_path = wget.download(photo_url, out=output_directory)
    else:
        target_file_path = output_directory + '/' + filename
    return target_file_path

count_unparsed = 0
errors = []
_files = list(os.walk('/var/vk-data'))
#shuffle(_files)

for d, dirs, files in _files:
    for f in files:
        #print f
        with open(os.path.join(d, f), 'r') as rf:
            try:
                profile_info = json.load(rf)
                if profile_info:
                    if u"deactivated" in profile_info[u'basic']:
                        continue
                    if u"camera" in profile_info[u'basic'][u"photo_max"]:
                        continue
                    
                    users = posts.find_one({u'uid': int(profile_info["basic"]["id"])})
                    if not users or u'face_features' not in users:
                        photo_url = profile_info[u'basic'][u"photo_max"]
                        target_file_path = wget_photo(photo_url, u'/var/vk-data/photos')
                        face_features = faceprocessor.get(target_file_path)
                    else:
                        continue
                    face_features = json.dumps(list(face_features))
                    #print face_features
                    if not users:   
                        post_data = {
                            u'uid': profile_info[u"basic"][u"id"],
                            u'face_features': face_features,
                        }
                        result = posts.insert_one(post_data)
                    elif 'uface_features' not in users:
                        users[u'face_features'] = face_features
                        db.posts.save(users)
                    print "add {}".format(profile_info[u"basic"][u"id"])
                    
            except Exception as e:
                print e
                errors.append((e, f))
                count_unparsed += 1

print count_unparsed
