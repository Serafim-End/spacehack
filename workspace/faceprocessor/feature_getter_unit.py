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
import vk_api
import numpy as np

client = MongoClient('localhost', 27017)
db = client['users_and_features']
posts = db.posts
faceprocessor = FaceProcessor()

vk_session = vk_api.VkApi(token='a74844d7722277b716bbd4037e1c0480a0a5f568fe3f9a356564f0b5d8f33b677bf47db9b4d201cb428cc',
                                            app_id='6008096', client_secret='YBDSuGrvsC8vccTlenk8')
vk_session.auth()
tools = vk_api.VkTools(vk_session)



def wget_photo(photo_url, output_directory='/var/vk-data/photos'):
    filename = photo_url.split('/')[-1]
    if not os.path.exists('{}/{}'.format(output_directory, filename)):
        target_file_path = wget.download(photo_url, out=output_directory)
    else:
        target_file_path = output_directory + '/' + filename
    return target_file_path

interesting_users = posts.find( {'bad_user': { '$exists': False}, 'face_features': { '$exists': False}, 'active_search_score': {"$ne" : 1}, 'city.id' : 1}, no_cursor_timeout=True).sort( [ (u"active_search_score", -1),])


for user in interesting_users:
    uid = user['uid']
    limit_count = 3
    avatars = tools.get_all('photos.get', limit_count, {'owner_id': uid, 'album_id': 'profile', 'rev': 1, 'count': limit_count})
    avatars_urls = []
    try:
        for avatar in avatars['items'][:limit_count]:
            photos_size = ''
            for key in avatar.keys():
                if 'photo' in key:
                    if int(key[6:]) > 400:
                        photos_sizes = key
                        break
            max_photo = photos_sizes
            avatars_urls.append(avatar[max_photo])
        face_features_list = []
        for photo_url in avatars_urls:
            try:
                target_file_path = wget_photo(photo_url, u'/var/vk-data/photos')
                face_features = faceprocessor.get(target_file_path)
                face_features_list.append(face_features)
            except Exception as e:
                print e
        if len(face_features_list) == 0:
            print 'No faces found {}'.format(user['uid'])
            user[u'bad_user'] = 1
            db.posts.save(user)
            continue
        mean_face_features = np.mean(np.stack(face_features_list), axis=0)
        mean_face_features = json.dumps(list(mean_face_features))
        user[u'face_features'] = mean_face_features
        user[u'version'] += 1
        db.posts.save(user)
        print "add {}".format(user['uid'])
    except Exception as e:
        user[u'bad_user'] = 1
        db.posts.save(user)
        print e


