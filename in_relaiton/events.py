import cPickle
# coding: utf-8

import json

import urllib2

import numpy as np
import pandas as pd

# coding: utf-8

from collections import defaultdict
from datetime import datetime
import time
import json

import gensim
import pymongo

import sklearn

from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2

from sklearn.decomposition import PCA


model = gensim.models.KeyedVectors.load_word2vec_format('web_0_300_20.bin.gz', binary=True)
w2v = dict(zip(model.index2word, model.syn0))

morph = pymorphy2.MorphAnalyzer()


# load it again
with open('pca_model.pkl', 'rb') as fid:
    pca_model = cPickle.load(fid)


mapping = {
    'ADJF': '_ADJ',
    'NOUN': '_NOUN',
    'INFN': '_VERB',
}

def prepare_word(w, mapping, word2vec_model):
    w = morph.parse(w)[0]
    if w.tag.POS in mapping:
        new_w = '{}{}'.decode('utf-8').format(w.normal_form, mapping[w.tag.POS])
        v = vector(new_w, word2vec_model)  
        return v, new_w
    return (None, None)

def w2v_transformation(data, word2vec_model):
    """
    transform the data - it can be pandas format or just array
    :param data: data - pandas, numpy, list
    :param word2vec_model
    :return: transformed_data
    """
    dim = len(word2vec_model.itervalues().next())

    train_vectors = []
    for i, s in enumerate(data):
        words = s.split(' ')

        words_vector = None
        words_count = 0

        new_s = []
        sentence_vector = []
        for w in words:
            v, new_w = prepare_word(w, mapping, word2vec_model)
            if new_w:
                new_s.append(new_w)
                
                if isinstance(v, np.ndarray):
                    words_count += 1

                    if isinstance(words_vector, np.ndarray):
                        words_vector = words_vector + v
                    else:
                        words_vector = v

        if isinstance(words_vector, np.ndarray) and words_count > 0:
            words_vector = words_vector / words_count
        else:
            words_vector = None

        if isinstance(words_vector, np.ndarray):
            train_vectors.append(words_vector)
            
#         tfidf = TfidfVectorizer(analyzer=lambda x: x)
#         tfidf.fit(new_s)
            
#         max_idf = max(tfidf.idf_)
#         word2weight = defaultdict(
#             lambda: max_idf,
#             [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()]
#         )
            
#         train_w2v_tfidf.append(
#             np.array(
#                 np.mean(
#                     [word2vec_model[w] * word2weight[w] for w in new_s if w in word2vec_model]
#                     or [np.zeros(dim)],
#                     axis=0
#                 )
#             )
#         )

#     train_vectors = np.array(train_vectors)
    return train_vectors
#     return np.array(train_w2v_tfidf)


def get_main_ohe(basics):

    v = []
    
    v.append(basics['id'])

        
    v.append(basics['sex'])
    
    city = basics['city']['id'] if 'city' in basics else -1
    v.append(city)

    country = basics['country']['id'] if 'country' in basics else -1
    v.append(country)
    
    photo = 1 if 'photo' in basics else 0
    v.append(photo)
    
    try:
        birthdate = (time.mktime(datetime.strptime(basics['bdate'], '%d.%m.%Y').timetuple())
                     if 'bdate' in basics else 788907600.0)
    except: 
        birthdate = 788907600.0
    v.append(birthdate)
    relation = basics['relation'] if 'relation' in basics else -1
    v.append(relation)
    
    university = basics['university'] if 'university' in basics else -1
    
    if 'about' in basics:
        transf = w2v_transformation([basics['about']], w2v)
        if transf is not None and len(transf) > 0:
            about = transf[0]
        else:
            about = np.zeros(300)
    else:
        about = np.zeros(300)
                
    v += list(about)
    return v


def get_basic_info(uid):
    import vk_api
    vk_session = vk_api.VkApi(token='a74844d7722277b716bbd4037e1c0480a0a5f568fe3f9a356564f0b5d8f33b677bf47db9b4d201cb428cc',
                                            app_id='6008096', client_secret='YBDSuGrvsC8vccTlenk8')
    vk_session.auth()
    tools = vk_api.VkTools(vk_session)
    FIELDS = 'user_id,first_name,last_name,deactivated,verified,blacklisted,sex,bdate,city,country,home_town,photo_50,photo_100,photo_200_orig,photo_200,photo_400_orig,photo_max,photo_max_orig,lists,domain,has_mobile,contacts,site,education,universities,schools,status,last_seen,followers_count,common_count,counters,occupation,nickname,relatives,relation,personal,connections,exports,wall_comments,activities,interests,music,movies,tv,books,games,about,quotes,timezone'
    user_data = vk_session.method('users.get', {'user_ids': uid, 'fields': FIELDS})[0]
    return user_data


def prepare_vector(uid):
    basic = get_basic_info(uid)
#     print basic
    profile_embedding = get_main_ohe(basic)
    interests_vector = list(pca_model.transform(profile_embedding)[0]) 
    return interests_vector


