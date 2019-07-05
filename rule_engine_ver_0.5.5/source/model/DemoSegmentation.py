#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:19:33 2019

@author: tungfint
"""

from flask_restful import Resource
from source.utilities.utils import Utils

class DemoSegmentation(Resource):
    @classmethod
    def make_api(cls, es, indexes):
        cls.es = es
        cls.indexes = indexes
        
    def get(self, assignmentID):
        _assignment = self.es.search(index=self.indexes['index_assignment'], body={ "query": { "ids" : { "values" : assignmentID } } })
        _assignment = _assignment['hits']['hits'][0]['_source']
        
        _segmentationId = _assignment['segmentationId']
        _contentId = _assignment['contentId']
        _expireAfter = _assignment['expireAfter']
        _validTo = _assignment['validTo']
        _competitionPoolID = _assignment['competitionPoolId']
        
        _content = self.es.search(index=self.indexes['index_content'], body={ "query": { "ids" : { "values" : _contentId } } })
        _content = _content['hits']['hits'][0]['_source']
        _competition_pool = self.es.search(index=self.indexes['index_competition_pool'], body={ "query": { "ids" : { "values" : _competitionPoolID } } })
        _competition_pool = _competition_pool['hits']['hits'][0]['_source']
        
        _createTime, _validTo = Utils.createTime_validTo(_validTo, _expireAfter)
        
        userIDs = Utils.executeSegmentation(self.es, self.indexes, _segmentationId)
        list_doc = []
        for userID in userIDs:
            if ( Utils.check_Limit_Content(self.es, self.indexes['index_assigned_content'], _content) and 
            Utils.check_Frequency_Content(self.es, self.indexes['index_assigned_content'], _content, _createTime) and
            Utils.check_Limit_CompetionPool(self.es, self.indexes['index_assigned_content'], _competition_pool, userID, _createTime) and
            Utils.check_Frequency_CompetionPool(self.es, self.indexes['index_assigned_content'], _competition_pool, _createTime) ):
                doc = {
                    'shopperId': userID,
                    'contentId': _contentId,
                    'segmentationId': _segmentationId,
                    'competitionPoolId': _competitionPoolID,
                    'createTime': _createTime,
                    'validTo': _validTo
                }
                self.es.index(index=self.indexes['index_assigned_content'], doc_type=self.indexes['type_assigned_content'], body=doc)
                self.es.indices.refresh(self.indexes['index_assigned_content'])                
                list_doc.append(doc)
        return list_doc, 200
        

