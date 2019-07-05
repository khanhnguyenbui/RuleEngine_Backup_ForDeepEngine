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
    def make_api(cls, es, indexes):
        cls.es = es
        cls.indexes = indexes
        
    def get(self, userID, perID):
        return Utils.executePersonalization(self.es, self.indexes, userID, perID)
    
    
    
