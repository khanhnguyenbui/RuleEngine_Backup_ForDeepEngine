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
        return Utils.executeSegmentation(self.es, self._index_query, self._index_seg, segID)
