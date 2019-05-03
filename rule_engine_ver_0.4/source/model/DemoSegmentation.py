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
    def make_api(cls, es, _index_query, _index_seg, _index_per, _index_assignedcontent, _type_assignedcontent):
        cls.es = es
        cls._index_query = _index_query
        cls._index_seg = _index_seg
        cls._index_per = _index_per
        cls._index_assignedcontent = _index_assignedcontent
        cls._type_assignedcontent = _type_assignedcontent        
        
    def get(self, segID, contentID):
        userIDs = Utils.executeSegmentation(self.es, self._index_query, self._index_seg, segID)
        list_doc = []
        for userID in userIDs:
            doc = {
                'shopperId': userID,
                'contentId': contentID,
                'segmentationId': segID
            }
            self.es.index(index=self._index_assignedcontent, doc_type=self._type_assignedcontent, body=doc)
            list_doc.append(doc)
        return list_doc, 200
        

