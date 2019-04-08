#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 01:20:53 2019

@author: thuanngo tungft

"""
from flask_restful import Resource
from source.utilities.utils import Utils

class Query(Resource):
    
    @classmethod
    def make_api(cls, request, es, _index_query,_doc_query):
        cls.request = request
        cls.es = es
        cls._index_query=_index_query
        cls._doc_query=_doc_query
        return cls
# Search a Query by queryID
    def get(self, queryID):
        res = self.es.search(index=self._index_query, body={ "query": { "ids" : { "values" : [queryID] } } })
        res = Utils.getActive(res)
        if (len(res) > 0):
            return res, 200
        return "Query not found", 404

# Create a new query, unique queryID
    def post(self, queryID):
        res = self.es.search(index=self._index_query, body={ "query": { "ids" : { "values" : [queryID] } } })
        res = Utils.getActive(res)
        if (len(res) > 0):
            return "Query already exists".format(queryID), 400
        inp = self.request.json
        print(inp)
        inp["dsl"] = Utils.jquerybuild2dsl(inp["content"])
        #inp.pop("queryID")
        inp['active'] = 1
        res = self.es.index(index=self._index_query, doc_type=self._doc_query, id = queryID, body=inp)
        return res["result"], 201

# Update a existing query
    def put(self, queryID):
        res = self.es.search(index=self._index_query, body={ "query": { "ids" : { "values" : [queryID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "User not exists", 404
        inp = self.request.json
        inp["dsl"] = Utils.jquerybuild2dsl(inp["content"])
        #inp.pop("queryID")
        inp['active'] = res[0]['_source']['active']
        res = self.es.index(index=self._index_query, doc_type=self._doc_query, id = queryID, body=inp)
        return res["result"], 202   
    
# Delete a existing query
    def delete(self, queryID):
        res = self.es.search(index=self._index_query, body={ "query": { "ids" : { "values" : [queryID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "User not exists", 404
        res[0]['_source']['active'] = 0
        res = self.es.index(index=self._index_query, doc_type=self._doc_query, id = queryID, body=res[0]['_source'])
        return "Deleted.", 202

# Get all query
class QueryAll(Resource):
    @classmethod
    def make_api(cls, es, _index_query):
        cls.es = es
        cls._index_query=_index_query;
        return cls
    def get(self):
        _query = {"query": { "match_all": { } } }
        res = self.es.search(index=self._index_query, body=_query)
        res = Utils.getActive(res)
        if (len(res) > 0):
            return res, 200
        return "Query not found", 404
    

#EXECUTE a seg in API- run a query in ES
class ExecuteQuery(Resource):
    
    @classmethod
    def make_api(cls, es,_index, _index_query):
        cls.es = es
        cls._index = _index
        cls._index_query=_index_query
        return cls
    #EXECUTE a seg - run a query in ES 
    def get(self, queryID):       
        return Utils.exeQuery(queryID, self.es,self._index, self._index_query)
       