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
        return Utils.executePersonalization(self.es, self._index_per, self._index_query, userID, perID)
    
    
    
