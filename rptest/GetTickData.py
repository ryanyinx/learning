#coding=utf-8

import requests
import demjson
import logging
import json
import time
from jsonpath_rw import jsonpath, parse
from time import sleep
import threading
from threading import Timer
import csv
import datetime


stockIDList = []
def getStockList(type):
    global headers
    # http://vip.newapi.wmcloud-stg.com/api/equity/getEqu.json?equTypeCD=A&listStatusCD=L,S
    response = requests.get('http://vip.newapi.wmcloud-stg.com/api/equity/getEqu.json?equTypeCD=A&listStatusCD=L,S')
    responseContent = response.content
    jsonpathExpression = parse('$.data[*].ticker')
    for match in jsonpathExpression.find(json.loads(responseContent)):
        stockIDList.append(match.value)

def getTickData(stockId):
    print stockId
    lastVolumn = 0
    fileName = 'd://tickdata//%s.csv' % stockId
    csvFile = file(fileName, 'wb')
    writer = csv.writer(csvFile)
    writer.writerow(['ticker', 'lastprice', 'volume'])
    csvFile.close()
    while True:
        response = requests.get('https://gw.wmcloud.com/ira/mobile/whitelist/stock/ticker?type=1&tickers=%s' % stockId)
        responseContent = response.content
        ticker = parse('$.tickRTSnapshotList.tickRTSnapshot[0].ticker').find(json.loads(responseContent))[0].value
        lastPrice = parse('$.tickRTSnapshotList.tickRTSnapshot[0].lastPrice').find(json.loads(responseContent))[0].value
        volumn = parse('$.tickRTSnapshotList.tickRTSnapshot[0].volume').find(json.loads(responseContent))[0].value
        # 上一次volumn不等于这次volumn 保存这个数据
        if lastVolumn != volumn:
            csvFile = open(fileName, 'a+')
            writer = csv.writer(csvFile)
            writer.writerow([ticker,lastPrice,volumn])
            csvFile.close()
        lastVolumn = volumn
        sleep(1)

def waitToTomorrow():
  tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1),
             hour=9, minute=10, second=0)
  delta = tomorrow - datetime.datetime.now()
  time.sleep(delta.seconds)

# writer = csv.writer(file('d://tickdata//000002.csv', 'wb'))
# writer.writerow(['Column1', 'Column2', 'Column3'])
# lines = [range(3) for i in range(5)]
# for line in lines:
#     writer.writerow(line)
waitToTomorrow()
env = 'stg'
tokenStg = 'e2d925633a85724ecab32d0e2bd70f09126899e5bc55438c5585354eb45404bd'
tokenPrd = ''
headers = {'Content-type':'application/json charset=utf-8',
           'Authorization': 'Bearer '+tokenStg}
if env == 'prd':
    headers = {'Content-type':'application/json',
           'Authorization': 'Bearer '+tokenPrd}
# 获取股票列表
getStockList('A')
stockIDList.append()
# 启动多线程获取tick数据
for stockId in stockIDList[0:10]:
    t = threading.Thread(target=getTickData, args=(stockId,))
    t.start()

