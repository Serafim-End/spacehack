# -*- coding: utf-8 -*-

import vk_api
import json
import time, random
import os, sys
import threading

FIELDS = 'user_id,first_name,last_name,deactivated,verified,blacklisted,sex,bdate,city,country,home_town,photo_50,photo_100,photo_200_orig,photo_200,photo_400_orig,photo_max,photo_max_orig,lists,domain,has_mobile,contacts,site,education,universities,schools,status,last_seen,followers_count,common_count,counters,occupation,nickname,relatives,relation,personal,connections,exports,wall_comments,activities,interests,music,movies,tv,books,games,about,quotes,timezone'

class MagicFetcher():
    def _do_call(self, kind, attr, *args, **kwargs):
        time.sleep(random.random())
        return getattr({'_tools': self._tools, '_vk_session': self._vk_session}[kind], attr)(*args, **kwargs)

    def _call(self, kind, attr, *args, **kwargs):
        for attempt in range(10):
            try:
                return self._do_call(kind, attr, *args, **kwargs)
            except Exception as e:
                print('    ', e, kind, attr, args, kwargs, file=sys.stderr)
        return None

    def get_profiles(self, user_id):
        #    friends = self._tools.get_all('friends.get', 1000, {'user_id': user_id})
        #    basic = self._vk_session.method('users.get', {'user_ids': user_id, 'fields': FIELDS})[0]
        #    wall = self._tools.get_all('wall.get', 1000, {'owner_id': user_id})
        basic = self._call('_vk_session', 'method', 'users.get', {'user_ids': ','.join(user_id), 'fields': FIELDS})
        #friends = self._call('_tools', 'get_all', 'friends.get', 1000, {'user_id': user_id})
        #wall = self._call('_tools', 'get_all', 'wall.get', 200, {'owner_id': user_id})
        return basic

    def __init__(self):
        try:
            self._vk_session = vk_api.VkApi(token='a74844d7722277b716bbd4037e1c0480a0a5f568fe3f9a356564f0b5d8f33b677bf47db9b4d201cb428cc',
                                            app_id='6008096', client_secret='YBDSuGrvsC8vccTlenk8')
            self._vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg, file=sys.stderr)
            return

        self._tools = vk_api.VkTools(self._vk_session)

def main():
    def worker():
        fetcher = MagicFetcher()
        while True:
            user_id = random.randint(1, 100000) * 1000
            base_path = '/var/vk-data-1000/'
            #dirname = os.path.join('/var/vk-data-1000', str(user_id)[-3:])
            #try:
            #    os.makedirs(dirname)
            #except FileExistsError:
            #    pass
            user_ids = list([str(i) for i in range(user_id, user_id + 1000)])
            file_path = os.path.join(base_path, 'profile-' + str(user_id) + '-' + str(user_id+1000) + '.json')
            if not os.path.exists(file_path):
                data_ = fetcher.get_profiles(user_ids)
                #print ('data', type(data_[0]))
                #print ('data', data_[0])
                json.dump(data_, open(file_path, 'w'), indent=4)
                print('Downloaded and saved user {}-{}'.format(user_id, user_id+1000), file=sys.stderr)

    for t in range(50):
        threading.Thread(target=worker).start()

if __name__ == '__main__':
    main()

