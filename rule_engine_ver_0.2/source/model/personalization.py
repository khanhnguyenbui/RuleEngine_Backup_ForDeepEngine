#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 03:51:26 2019

@author: thuanngo tungfint
"""
from flask_restful import Resource
from source.utilities.utils import Utils

class Personalization(Resource):
    @classmethod
    def make_api(cls, request, es,_index_per, _doc_per):
        cls.request = request
        cls.es = es
        cls._index_per = _index_per
        cls._doc_per = _doc_per
        return cls
# Search a personalization by perID
    def get(self, perID):
        res = self.es.search(index=self._index_per, body={ "query": { "ids" : { "values" : [perID] } } })
        res = Utils.getActive(res)
        if (len(res) > 0):
            return res, 200
        return "Personalization not found", 404

# Create a new per, unique perID
    def post(self, perID):
        res = self.es.search(index=self._index_per, body={ "query": { "ids" : { "values" : [perID] } } })
        res = Utils.getActive(res)
        if (len(res) > 0):
            return "perID already exists", 400
        inp = self.request.json
        inp["active"] = 1
        res = self.es.index(index=self._index_per, doc_type=self._doc_per, id = perID, body=inp)
        return res["result"], 201

# Update a existing seg
    def put(self, perID):
        res = self.es.search(index=self._index_per, body={ "query": { "ids" : { "values" : [perID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "perID not found", 400
        inp = self.request.json
        inp["active"] = res[0]['_source']['active']
        res = self.es.index(index=self._index_per, doc_type=self._doc_per, id = perID, body=inp)
        return res["result"], 202
    
# Delete a existing seg
    def delete(self, perID):
        res = self.es.search(index=self._index_per, body={ "query": { "ids" : { "values" : [perID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "perID not found", 400
        res[0]['_source']['active'] = 0
        res = self.es.index(index=self._index_per, doc_type=self._doc_per, id = perID, body=res[0]['_source'])
        return "Deleted.", 202

# Get all personalization
class PerAll(Resource):
    @classmethod
    def make_api(cls, es,_index_per):
        cls.es = es
        cls._index_per = _index_per
        return cls
    
    def get(self):
        _query = {"query": { "match_all": { } } }
        res = self.es.search(index=self._index_per, body=_query)
        res = Utils.getActive(res)
        if (len(res) > 0):
            return res, 200
        return "perID not found", 400
    
#EXECUTE a seg - run a query in ES
class ExecutePersonalization(Resource):
    
    @classmethod
    def make_api(cls, es, _index_per, _index_query):
        cls.es = es
        cls._index_per = _index_per
        cls._index_query = _index_query
        
    def get(self, userID, perID):
        res = self.es.search(index=self._index_per, body={ "query": { "ids" : { "values" : [perID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "perID not found", 400
        per = res[0]["_source"]["content"]
        totalPoint = 0
        for p in per:
            list_queryID = p['list_queryID']
            point = p['point']
            totalPoint = totalPoint + self.calPoint(userID, list_queryID, point)
        return totalPoint
    
    def calPoint(self, userID, list_queryID, point):
        res = Utils.exeMultiQuery(list_queryID, self.es, self._index_query)
        if userID in res: 
            return point
        return 0