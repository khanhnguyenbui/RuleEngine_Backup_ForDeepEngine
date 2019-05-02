#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:12:42 2019

@author: vanthuanngo tungfint
"""
from flask_restful import Resource, reqparse
from source.utilities.utils import Utils

class User(Resource):
    
    @classmethod
    def make_api(cls, es, _index, _doc_type):
        cls.es = es
        cls._index=_index;
        cls._doc_type=_doc_type;
        return cls
    # Search user by userID
    def get(self, userID ):
        if userID is None:
            _query = {"query": { "match_all": { } } }
            res = self.es.search(index=self._index, body=_query)
            res = Utils.getActive(res)
            if len(res) > 0: 
                return res, 200
            return 0
        else:
            res = self.es.search(index=self._index, body={ "query": { "ids" : { "values" : [userID] } } })
            res = Utils.getActive(res)
            if (len(res) > 0):
                return res, 200
            return "UserID not found", 404

# Create a new user, unique userID
    def post(self, userID):
        res = self.es.search(index=self._index, body={ "query": { "ids" : { "values" : [userID] } } })
        res = Utils.getActive(res)
        if (len(res) > 0):
            return "UserID already exists", 400
        
        parser = reqparse.RequestParser()
        parser.add_argument("birthDate")
        parser.add_argument("birthMonth")
        parser.add_argument("birthYear")
        parser.add_argument("firstName")
        parser.add_argument("lastName")
        args = parser.parse_args()
     
        user = {
            "birthDate": args["birthDate"],
            "birthMonth": args["birthMonth"],
            "birthYear": args["birthYear"],
            "firstName": args["firstName"],
            "lastName": args["lastName"],
        }
        user['active'] = 1
        res = self.es.index(index=self._index, doc_type=self._doc_type, id = userID, body=user)

        return res["result"], 201

# Update the information about an existing username
    def put(self, userID):
        res = self.es.search(index=self._index, body={ "query": { "ids" : { "values" : [userID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "UserID not exists", 404
        
        parser = reqparse.RequestParser()
        parser.add_argument("birthDate")
        parser.add_argument("birthMonth")
        parser.add_argument("birthYear")
        parser.add_argument("firstName")
        parser.add_argument("lastName")
        args = parser.parse_args()
     
        user = {
            "birthDate": args["birthDate"],
            "birthMonth": args["birthMonth"],
            "birthYear": args["birthYear"],
            "firstName": args["firstName"],
            "lastName": args["lastName"],
        }
        user['active'] = res[0]['_source']['active']
        res = self.es.index(index=self._index, doc_type=self._doc_type, id = userID, body=user)
        
        return res["result"], 200
            
# Delete a user
    def delete(self, userID):
        res = self.es.search(index=self._index, body={ "query": { "ids" : { "values" : [userID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "UserID not exists", 404
        res[0]['_source']['active'] = 0
        self.es.index(index=self._index, doc_type=self._doc_type, id = userID, body = res[0]['_source'])
        return "Deleted.".format(userID), 200
        
class UserAll(Resource):
 
    
    def get(self):
        _query = {"query": { "match_all": { } } }
        res = self.es.search(index=self._index, body=_query)
        return res
    
    @classmethod
    def make_api(cls, es, _index):
        cls.es = es
        cls._index=_index;
        return cls