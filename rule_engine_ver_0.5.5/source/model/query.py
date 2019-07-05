#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 01:20:53 2019

@author: thuanngo tungfint

"""
from flask_restful import Resource
from source.utilities.utils import Utils

# Get all query
class QueryAll(Resource):
    @classmethod
    def make_api(cls, es, indexes):
        cls.es = es
        cls.indexes = indexes;
        return cls
    
    def get(self):
        _query = {"query": { "match_all": { } } }
        res = self.es.search(index=self.indexes['index_query'], body=_query)
        res = Utils.getActive(res)
        if (len(res) > 0):
            return res, 200
        return "Query not found", 404
    

#EXECUTE a seg in API- run a query in ES
class ExecuteQuery(Resource):
    
    @classmethod
    def make_api(cls, es, indexes):
        cls.es = es
        cls.indexes = indexes
        return cls
    
    #EXECUTE a seg - run a query in ES 
    def get(self, queryID):       
        return Utils.exeQuery(queryID, self.es, self.indexes['index_query'])
       