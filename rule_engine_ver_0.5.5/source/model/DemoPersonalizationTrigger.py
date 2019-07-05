#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:17:39 2019

@author: tungfint
"""

from flask_restful import Resource
from source.utilities.utils import Utils

class DemoPersonalizationTrigger(Resource):
    @classmethod
    def make_api(cls, es, indexes):
        cls.es = es
        cls.indexes = indexes
    
    def get(self, userID, triggerID):
        assignments = self.es.search(index=self.indexes['index_assignment'], body={ "query": { "match_phrase" : { "triggerId" : triggerID } } })
        assignments = assignments['hits']['hits']
        
        __assignments = []
        for assignment in assignments:
            assignment = assignment['_source']
            if (assignment.get('personalizationId') != None):
                assignment['point'] = Utils.executePersonalization(self.es, self.indexes, userID, assignment['personalizationId'])
                __assignments.append(assignment)
        __assignments = sorted(__assignments, key = lambda i: i['point'], reverse=True) #sorting by point in descending order
        for assignment in __assignments:
            _contentId = assignment['contentId']
            _expireAfter = assignment['expireAfter']
            _validTo = assignment['validTo']
            _competitionPoolID = assignment['competitionPoolId']
            _personalizationId = assignment['personalizationId']
            
            _content = self.es.search(index=self.indexes['index_content'], body={ "query": { "ids" : { "values" : _contentId } } })
            _content = _content['hits']['hits'][0]['_source']
            _assigned_content = self.es.search(index=self.indexes['index_assigned_content'], body={ "query": { "match_phrase" : { "contentId" : _contentId } } })
            _assigned_content = _assigned_content['hits']['hits']
            _competition_pool = self.es.search(index=self.indexes['index_competition_pool'], body={ "query": { "ids" : { "values" : _competitionPoolID } } })
            _competition_pool = _competition_pool['hits']['hits'][0]['_source']
        
            _createTime, _validTo = Utils.createTime_validTo(_validTo, _expireAfter)
                
            if ( Utils.check_Limit_Content(self.es, self.indexes['index_assigned_content'], _content) and 
            Utils.check_Frequency_Content(self.es, self.indexes['index_assigned_content'], _content, _createTime) and
            Utils.check_Limit_CompetionPool(self.es, self.indexes['index_assigned_content'], _competition_pool, userID, _createTime) and
            Utils.check_Frequency_CompetionPool(self.es, self.indexes['index_assigned_content'], _competition_pool, _createTime) ):
                doc = {
                    'shopperId': userID,
                    'contentId': _contentId,
                    'personalizationId': _personalizationId,
                    'competitionPoolId': _competitionPoolID,
                    'createTime': _createTime,
                    'validTo': _validTo
                }
                self.es.index(index=self.indexes['index_assigned_content'], doc_type=self.indexes['type_assigned_content'], body=doc)
                self.es.indices.refresh(self.indexes['index_assigned_content'])  
                return doc, 200
    
#from elasticsearch import Elasticsearch
#es = Elasticsearch( hosts = [{'host': '35.237.224.155', 'port': 9200}])
#res = es.search(index="assigned_contents", body={ "query": { "match_phrase" : { "shopperId" : "sushix2@gmail.com"} } })
#print(res)


