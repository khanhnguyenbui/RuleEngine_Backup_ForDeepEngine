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
            if r['_source'].get('active') == None or r['_source']['active'] > 0:
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
        _body = Utils.jquerybuild2dsl(res[0]["_source"]["queryBody"])
        res = es.search(index=res[0]["_source"]["indexName"], body=_body)
        if (res['hits']['total'] > 0):
            res = res["hits"]["hits"]
            for r in res:
                listID.append(r["_source"]["shopperId"])
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

### Execute Personalization
    def calPoint(es, userID, list_queryID, point, _index_query):
        res = Utils.exeMultiQuery(list_queryID, es, _index_query)
        if userID in res: 
            return point
        return 0
    
    def executePersonalization(es, _index_per, _index_query, userID, perID):
        res = es.search(index=_index_per, body={ "query": { "ids" : { "values" : [perID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "perID not found", 400
        per = res[0]["_source"]["scoredQuerieIds"]
        totalPoint = 0
        for p in per:
            list_queryID = p['queryIds']
            point = p['point']
            totalPoint = totalPoint + Utils.calPoint(es, userID, list_queryID, point, _index_query)
        return totalPoint
    
### Execute Segmentation
    def executeSegmentation(es, _index_query, _index_seg, segID):
        res = es.search(index=_index_seg, body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "segID not found", 400
        list_queryID = res[0]["_source"]["queryIds"]
        res = Utils.exeMultiQuery(list_queryID, es, _index_query)
        return res
    
