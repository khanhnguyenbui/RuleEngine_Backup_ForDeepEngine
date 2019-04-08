#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 01:44:46 2019

@author: thuanngo tungft

"""
from flask_restful import Resource
from source.utilities.utils import Utils

class Segmentation(Resource):
    @classmethod
    def make_api(cls, request, es,_index_seg, _doc_seg):
        cls.request = request
        cls.es = es
        cls._index_seg = _index_seg
        cls._doc_seg = _doc_seg
        return cls
# Search a segmentation by segID
    def get(self, segID):
        res = self.es.search(index=self._index_seg, body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) > 0):
            return res, 200
        return "Segmentation not found", 404

# Create a new seg, unique segID
    def post(self, segID):
        res = self.es.search(index=self._index_seg, body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) > 0):
            return "segID already exists", 400
        inp = self.request.json
        inp['active'] = 1
        res = self.es.index(index=self._index_seg, doc_type=self._doc_seg, id = segID, body=inp)
        return res["result"], 201

# Update a existing seg
    def put(self, segID):
        res = self.es.search(index=self._index_seg, body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "segID not found", 400
        inp = self.request.json
        inp['active'] = res[0]['_source']['active']
        res = self.es.index(index=self._index_seg, doc_type=self._doc_seg, id = segID, body=inp)
        return res["result"], 202
    
# Delete a existing seg
    def delete(self, segID):
        res = self.es.search(index=self._index_seg, body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "segID not found", 400
        res[0]['_source']['active'] = 0
        res = self.es.index(index=self._index_seg, doc_type=self._doc_seg, id = segID, body=res[0]['_source'])
        return "Deleted.", 202

# Get all segmentation
class SegAll(Resource):
    @classmethod
    def make_api(cls, es,_index_seg):
        cls.es = es
        cls._index_seg = _index_seg
        return cls
    def get(self):
        _query = {"query": { "match_all": { } } }
        res = self.es.search(index=self._index_seg, body=_query)
        res = Utils.getActive(res)
        if (len(res) > 0):
            return res, 200
        return "segID not found", 400
    
#EXECUTE a seg - run a query in ES
class ExecuteSegmentation(Resource):
    @classmethod
    def make_api(cls, es,_index_seg,_index,_index_query):
        cls.es = es
        cls._index_seg = _index_seg
        cls._index = _index
        cls._index_query = _index_query
    def get(self, segID):
        res = self.es.search(index=self._index_seg, body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "segID not found", 400
        queryID = res[0]["_source"]["queryID"]
        return Utils.exeQuery(queryID, self.es,self._index, self._index_query)
