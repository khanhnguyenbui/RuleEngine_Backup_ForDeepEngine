#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:36:11 2019

@author: thuanngo tungfint

"""
import source.utilities.jquerybuilder2elasticquery
from querybuilder.rules import Rule

class Utils:
    def getActive(listRes):
        res = list()
        if listRes['hits']['total'] == 0:
            return res
        listRes = listRes['hits']['hits']
        for r in listRes:
            if r['_source']['active'] > 0:
                res.append(r)
        return res
    
    def jquerybuild2dsl(jsonRule):
        jqueryRule = Rule(jsonRule)
        q = source.utilities.jquerybuilder2elasticquery.to_esl_query(jqueryRule)
        res = q.to_dict()
        res = {'query': res}
        return res
    
    
    #intersection of two lists
    def intersection(l1, l2): 
        l3 = [value for value in l1 if value in l2] 
        return l3

    #EXECUTE a query - run a query in ES 
    def exeQuery(queryID, es, _index_query):
        res = es.search(index=_index_query, body={ "query": { "ids" : { "values" : [queryID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0): 
            return "Query not found", 404
        
        listID = list()
        res = es.search(index=res[0]["_source"]["r_index"], body=res[0]["_source"]["dsl"])
        if (res['hits']['total'] > 0):
            res = res["hits"]["hits"]
            for r in res:
                listID.append(r["_id"])
        return listID

    #EXECUTE multi query
    def exeMultiQuery(list_queryID, es, _index_query):
        listRes = list()
        for queryID in list_queryID:
            res = Utils.exeQuery(queryID, es, _index_query)
            if (listRes == []):
                listRes = res
            else:
                listRes = Utils.intersection(listRes, res)
        return listRes
    
