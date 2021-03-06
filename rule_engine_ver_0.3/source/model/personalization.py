#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 03:51:26 2019

@author: thuanngo tungfint
"""
from flask_restful import Resource
from source.utilities.utils import Utils

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
        per = res[0]["_source"]["scoredQuerieIds"]
        totalPoint = 0
        for p in per:
            list_queryID = p['queryIds']
            point = p['point']
            totalPoint = totalPoint + self.calPoint(userID, list_queryID, point)
        return totalPoint
    
    def calPoint(self, userID, list_queryID, point):
        res = Utils.exeMultiQuery(list_queryID, self.es, self._index_query)
        if userID in res: 
            return point
        return 0
    
