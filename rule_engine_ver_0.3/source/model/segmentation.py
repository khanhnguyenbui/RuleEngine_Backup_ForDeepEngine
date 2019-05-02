#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 01:44:46 2019

@author: thuanngo tungfint
"""
from flask_restful import Resource
from source.utilities.utils import Utils
  
#EXECUTE a seg - run a query in ES
class ExecuteSegmentation(Resource):
    @classmethod
    def make_api(cls, es, _index_seg, _index_query):
        cls.es = es
        cls._index_seg = _index_seg
        cls._index_query = _index_query
        
    def get(self, segID):
        res = self.es.search(index=self._index_seg, body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "segID not found", 400
        list_queryID = res[0]["_source"]["queryIds"]
        res = Utils.exeMultiQuery(list_queryID, self.es, self._index_query)
        return res
