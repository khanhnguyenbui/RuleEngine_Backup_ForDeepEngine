#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:17:39 2019

@author: tungfint
"""

import operator
from flask_restful import Resource
from source.utilities.utils import Utils

class DemoPersonalizationTrigger(Resource):
    @classmethod
    def make_api(cls, es, _index_query, _index_assignment, _index_per, _index_assignedcontent, _type_assignedcontent):
        cls.es = es
        cls._index_query = _index_query
        cls._index_assignment = _index_assignment
        cls._index_per = _index_per
        cls._index_assignedcontent = _index_assignedcontent
        cls._type_assignedcontent = _type_assignedcontent  
        
        
    def get(self, userID, triggerID):
#        print(111111111111111111)
#        triggerID = 'trigger1'
        res = self.es.search(index=self._index_assignment, body={ "query": { "term" : { "triggerId" : triggerID } } })
#        res = es.search(index='assignments', body={ "query": { "term" : { "triggerId" : triggerID } } })
#        print(res)
        res = res['hits']['hits']
        PersonalizationIds = [r['_source']['personalizationId'] for r in res]
        print(PersonalizationIds)
        Points = {}
#        for perID in PersonalizationIds:
#            Points[perID] = ExecutePersonalization.get(userID, perID)
        
        
        Points = {perID : Utils.executePersonalization(self.es, self._index_per, self._index_query, userID, perID) for perID in PersonalizationIds}
        
        perId_max = max(Points.items(), key=operator.itemgetter(1))[0]
        
        for r in res:
            per = r['_source']
            if per['personalizationId'] == perId_max:
                _contentId = per['contentId']
                break
        doc = {
            'shopperId': userID,
            'contentId': _contentId,
            'personalizationId': perId_max
        }
        res = self.es.index(index=self._index_assignedcontent, doc_type=self._type_assignedcontent, body=doc)
        return doc, 200

#es = Elasticsearch( hosts = [{'host': '35.237.224.155', 'port': 9200}])


