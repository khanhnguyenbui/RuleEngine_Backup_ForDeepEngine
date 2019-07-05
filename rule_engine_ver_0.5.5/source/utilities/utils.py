#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:36:11 2019

@author: thuanngo tungfint

"""
import source.utilities.jquerybuilder2elasticquery
from querybuilder.rules import Rule
import datetime
import pytz

class Utils:
    system_time = "GMT+7"
    formatTime = '%Y-%m-%dT%H:%M:%SZ'
    
    def getTimeZone():
        sysTime = Utils.system_time
        if '+' in sysTime: _timezone = "Etc/" + sysTime.replace('+','-')
        else: _timezone = "Etc/" + sysTime.replace('-','+')
        return _timezone
    
    frequencyUnit = {
        'day': 1,
        'week': 7,
        'month': 30,
        'year': 365,
    }
    
    def getActive(listRes):
        res = list()
        if listRes['hits']['total'] == 0:
            return res
        listRes = listRes['hits']['hits']
#        for r in listRes:
#            if r['_source'].get('active') == None or r['_source']['active'].lower() != "false" or r['_source']['active'].lower() != "0":
#                res.append(r)
        return listRes
    
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
    def exeQuery(queryID, es, index_query):
        res = es.search(index=index_query, body={ "query": { "ids" : { "values" : queryID } } })
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
    def exeMultiQuery(list_queryID, es, index_query):
        listRes = list()
        flag = True
        for queryID in list_queryID:
            res = Utils.exeQuery(queryID, es, index_query)
            if (flag):
                listRes = res
                flag = False
            else:
                listRes = Utils.intersection(listRes, res)
        return listRes

### Execute Personalization
    def calPoint(es, userID, queryID, point, indexes):
        res = Utils.exeQuery(queryID, es, indexes['index_query'])
       
        if userID in res: 
            return point
        return 0
    
    def executePersonalization(es, indexes, userID, perID):
        res = es.search(index=indexes['index_personalization'], body={ "query": { "ids" : { "values" : perID } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "perID not found", 400
        per = res[0]["_source"]["scoredQuerieIds"]
        totalPoint = 0
        for p in per:
            queryID = p['queryIds']
            if (p.get('required') != None and p['required'].lower() == 'true'):
                res = Utils.exeQuery(queryID, es, indexes['index_query'])
                if not userID in res: 
                    return 0
            
            point = p['point']
            totalPoint = totalPoint + Utils.calPoint(es, userID, queryID, point, indexes)

        return totalPoint
    
### Execute Segmentation
    def executeSegmentation(es, indexes, segID):
        res = es.search(index=indexes['index_segmentation'], body={ "query": { "ids" : { "values" : [segID] } } })
        res = Utils.getActive(res)
        if (len(res) == 0):
            return "segID not found", 400
        list_queryID = res[0]["_source"]["queryIds"]
        res = Utils.exeMultiQuery(list_queryID, es, indexes['index_query'])
        return res
    
### DEMO SEGMENTATION & PERSONALIZATION ###    
    
    def createTime_validTo(_validTo, _expireAfter):
        _timezone = Utils.getTimeZone()
        currentTime = datetime.datetime.now(pytz.timezone(_timezone)).strftime(Utils.formatTime)
        currentTime = datetime.datetime.strptime(currentTime, Utils.formatTime)
        _createTime = currentTime.strftime(Utils.formatTime)
        
        _validTo = datetime.datetime.strptime(_validTo, Utils.formatTime)
        _validTo = min(_validTo, currentTime + datetime.timedelta(days = _expireAfter))
        _validTo = _validTo.strftime(Utils.formatTime)
        
        return _createTime, _validTo
    
    def check_Limit_Content(es, _index_assigned_content, _content): # limit of this content
        _assigned_content = es.search(index=_index_assigned_content, body={ "query": { "match_phrase" : { "contentId" : _content['contentId'] } } })
        _assigned_content = _assigned_content['hits']['hits']
        _limit_content = _content['limit']
        if len(_assigned_content) < _limit_content: 
#            print('Limit_Content: pass')
            return True
#        print('Limit_Content: not pass')
        return False
    
    def check_Frequency_Content(es, _index_assigned_content, _content, currentTime): # Frequency of this content, how many this content per days
        _assigned_content = es.search(index=_index_assigned_content, body={ "query": { "match_phrase" : { "contentId" : _content['contentId'] } } })
        _assigned_content = _assigned_content['hits']['hits']
        numbers_of_content = _content['frequencyNumber']
        numbers_of_day = Utils.frequencyUnit[_content['frequencyUnit']]
        
        count = 0
        for ac in _assigned_content:
            ac_createTime = datetime.datetime.strptime(ac['_source']['createTime'], Utils.formatTime)
            if (ac_createTime >= datetime.datetime.strptime(currentTime, Utils.formatTime) - datetime.timedelta(days = numbers_of_day)): count += 1
        if count < numbers_of_content:
#            print('Frequency_Content: pass')
            return True
#        print('Frequency_Content: not pass')
        return False
    
    def check_Limit_CompetionPool(es, _index_assigned_content, _competitionPool, userID, currentTime): # limit of content per a shopper
        _limit = _competitionPool['limit']
        _overwriteFlag = _competitionPool['overwriteFlag']
        _body = {
          "query": {
            "bool" : {
              "must" : [
                {"match_phrase" : { "shopperId" : userID }},
                {"match_phrase" : { "competitionPoolId" : _competitionPool['competitionPoolId'] }}
              ]
            }
          }
        }
        _assigned_content = es.search(index=_index_assigned_content, body=_body)
        _assigned_content = _assigned_content['hits']['hits']
        if _overwriteFlag.lower() == 'false':
#            print(_limit - len(_assigned_content) > 0)
            return (_limit - len(_assigned_content) > 0)
        for ac in _assigned_content:
            _limit -= ( datetime.datetime.strptime(currentTime, Utils.formatTime) < (datetime.datetime.strptime(ac['_source']['validTo'], Utils.formatTime)) )
#        print(_limit > 0)
        return (_limit > 0)
    
    def check_Frequency_CompetionPool(es, _index_assigned_content, _competitionPool, currentTime): # Frequency of content, how many content per days with a CompetionPool
        _assigned_content = es.search(index=_index_assigned_content, body={ "query": { "match_phrase" : { "competitionPoolId" : _competitionPool['competitionPoolId'] } } })
        _assigned_content = _assigned_content['hits']['hits']
        numbers_of_content = _competitionPool['frequencyNumber']
        numbers_of_day = Utils.frequencyUnit[_competitionPool['frequencyUnit']]
        
        count = 0
        for ac in _assigned_content:
            ac_createTime = datetime.datetime.strptime(ac['_source']['createTime'], Utils.formatTime)
            if (ac_createTime >= datetime.datetime.strptime(currentTime, Utils.formatTime) - datetime.timedelta(days = numbers_of_day)): count += 1

        if count < numbers_of_content:
#            print('Frequency_CompetionPool: pass')
            return True
#        print('Frequency_CompetionPool: not pass')
        return False
    