#coding=utf-8

import requests
import json
import time
from jsonpath_rw import jsonpath, parse
from time import sleep
import threading
import csv
from datetime import datetime, timedelta
import os

stockIDList = []
def getStockList(type):
    global headers
    # http://vip.newapi.wmcloud-stg.com/api/equity/getEqu.json?equTypeCD=A&listStatusCD=L,S
    response = requests.get('http://vip.newapi.wmcloud-stg.com/api/equity/getEqu.json?equTypeCD=%s&listStatusCD=L,S' % type)
    responseContent = response.content
    jsonpathExpression = parse('$.data[*].ticker')
    for match in jsonpathExpression.find(json.loads(responseContent)):
        stockIDList.append(match.value)

env = 'stg'
tokenStg = 'e2d925633a85724ecab32d0e2bd70f09126899e5bc55438c5585354eb45404bd'
tokenPrd = ''
headers = {'Content-type':'application/json charset=utf-8',
           'Authorization': 'Bearer '+tokenStg}
if env == 'prd':
    headers = {'Content-type':'application/json',
               'Authorization': 'Bearer '+tokenPrd}
getStockList('A')
for stockID in stockIDList:
    response = requests.get('https://gw.wmcloud-stg.com/rrpqa/web/holderShareChg?ticker=%s&pageNow=2&pageSize=10' % stockID, headers=headers)
    jsonPathExpression = parse('$.data.list[*].seniorName')
    # print stockID
    for match in jsonPathExpression.find(json.loads(response.content)):
        # print match.value + str(len(match.value))
        if len(match.value) > 3:
            print stockID