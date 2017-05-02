import os
import json
import pickle

import xgboost as xgb
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

import pymongo
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
import bson


client = MongoClient()
db = client.dataframe
db.embeddings.count()


def embedding():
    embs = []

    for e in db.embeddings.find({}):
        for vs in e.values():
            if isinstance(vs, ObjectId):
                continue
            else:
                ev = vs
    
        embs.append(ev)
    return np.array(embs)


def create_df(embs):
    columns = range(embs.shape[1])
    columns[78] = 'sex'
    columns[0] = 'user_id'
    
    df = pd.DataFrame(data=embs, columns=columns)
    
    # anti_set = pd.concat([df[df['sex']==u'4'], df[df['sex']==u'2'],  df[df['sex']==u'3']])
    return df

def tr_te_xgb(X_train, X_test, y_train, y_test):
    dtrain = xgb.DMatrix(X_train.as_matrix(), label=y_train)
    dtest = xgb.DMatrix(X_test.as_matrix(), label=y_test)
    return dtrain, dtest


def make_model(df, fname='in_relation_xgb.model'):
    
    df_prediction = df.copy()
    y = df_prediction[['user_id', 'sex']].set_index('user_id')
    y['sex'] = y.sex.apply(lambda x: 1 if x in [u'4', u'3', u'2'] else 0)
    del df_prediction['sex']
    
    df_prediction = df_prediction.set_index('user_id')
    X_train, X_test, y_train, y_test = train_test_split(df_prediction, y, test_size=0.2, random_state=42)
    d_train, d_test = tr_te_xgb(X_train, X_test, y_train, y_test)
    
    param = {
        'bst:max_depth':5,
        'bst:eta':1,
        'gamma': 2.,
        'scale_pos_weight':0.8,
        'lambda': 2.,
        'alpha':2.,
        'booster': 'dart',
        'objective':'binary:logistic' 
    }

    param['eval_metric'] = 'auc'
    param['nthread'] = 4

    evallist  = [(d_test,'eval'), (d_train,'train')]

    num_round = 20
    bst = xgb.train(param, d_train, num_round, evallist, )
    preds = bst.predict(d_test, ntree_limit=num_round)
    
    if fname:
        bst.save_model(fname)
        # pks = pickle.dump(bst, open(fname))

def make_model_upd(df, fname='in_relation_xgb.model', params=None):
    
    df_prediction = df.copy()
    df_prediction = df_prediction[df_prediction['sex'] != '0.0']
    y = df_prediction[['user_id', 'sex']].set_index('user_id')
    y['sex'] = y.sex.apply(lambda x: 1 if x in ['6.0'] else 0)
    del df_prediction['sex']
    
    df_prediction = df_prediction.set_index('user_id')
    X_train, X_test, y_train, y_test = train_test_split(df_prediction, y, test_size=0.2, random_state=42)
    d_train, d_test = tr_te_xgb(X_train, X_test, y_train, y_test)
    
    if not params:
        param = {
            'bst:max_depth':5,
            'bst:eta':1,
            'gamma': 2.,
            'scale_pos_weight':0.8,
            'lambda': 2.,
            'alpha':2.,
            'booster': 'dart',
            'objective':'binary:logistic' 
        }
    else:
        param = params

    param['eval_metric'] = 'auc'
    param['nthread'] = 4

    evallist  = [(d_test,'eval'), (d_train,'train')]

    num_round = 30
    bst = xgb.train(param, d_train, num_round, evallist, )
    preds = bst.predict(d_test, ntree_limit=num_round)
    
    if fname:
        bst.save_model(fname)
        # pks = pickle.dump(bst, open(fname, 'a'))
        
def make_prediction(df, fname='in_relation_xgb.model'):
    df_copy = df.copy()
    
    bst_loaded = pickle.load(file=open(fname))
    bst
    if 'sex' in df_copy:
        del df_copy['sex']
        
    return bst_loaded.predict(df_copy)
