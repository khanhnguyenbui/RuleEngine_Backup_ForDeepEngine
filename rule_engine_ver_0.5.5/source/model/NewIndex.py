#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 01:20:53 2019

@author: thuanngo tungfint

"""
from flask_restful import Resource

# add new doc into Index
class NewIndex(Resource):
    @classmethod
    def make_api(cls, es, request):
        cls.es = es
        cls.request = request
        return cls
    
    def post(self):
        inp = self.request.json
        _index = inp["indexName"]
        _doc = _index + 's'
        #if not self.es.indices.exists(index=indexName):
        #print(inp)
        res = self.es.index(index=_index, doc_type=_doc, body=inp)
        return res["result"], 201


       