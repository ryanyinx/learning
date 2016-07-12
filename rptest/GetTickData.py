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
    response = requests.get('http://vip.newapi.wmcloud-stg.com/api/equity/getEqu.json?equTypeCD=A&listStatusCD=L,S')
    responseContent = response.content
    jsonpathExpression = parse('$.data[*].ticker')
    for match in jsonpathExpression.find(json.loads(responseContent)):
        stockIDList.append(match.value)

def getTickData(stockId, hour, minute, endTime):
    # while True:
        print stockId
        # 当前时间比期望监测时间晚，则从下一天开始监测
        plusDay = 0
        if datetime.now().hour >= hour and datetime.now().minute >= minute:
            plusDay = 1
        waitToSomeTime(plusDay, hour, minute, 0)
        print 'from %s:%s to %s' % (hour, minute, endTime)
        lastVolumn = -1
        now = datetime.now()
        nowTime = now.strftime('%Y-%m-%d')
        folderName = 'd://tickdata//%s' % nowTime
        if not os.path.exists(folderName):
            os.mkdir(folderName, 07777)
        fileName = '%s//%s-%s.csv' % (folderName, stockId, endTime.replace(':', ''))
        csvFile = file(fileName, 'wb')
        writer = csv.writer(csvFile)
        writer.writerow(['time', 'ticker', 'lastprice', 'volume'])
        csvFile.close()
        while str(endTime) != str(nowTime):
            response = requests.get('https://gw.wmcloud.com/ira/mobile/whitelist/stock/ticker?type=1&tickers=%s' % stockId)
            responseContent = response.content
            nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ticker = parse('$.tickRTSnapshotList.tickRTSnapshot[0].ticker').find(json.loads(responseContent))[0].value
            lastPrice = parse('$.tickRTSnapshotList.tickRTSnapshot[0].lastPrice').find(json.loads(responseContent))[0].value
            volumn = parse('$.tickRTSnapshotList.tickRTSnapshot[0].volume').find(json.loads(responseContent))[0].value
            # 上一次volumn不等于这次volumn 保存这个数据
            if lastVolumn != volumn:
                csvFile = open(fileName, 'a+')
                writer = csv.writer(csvFile)
                writer.writerow([nowTime, ticker,lastPrice,volumn])
                csvFile.close()
            lastVolumn = volumn
            sleep(1)
            nowTime = datetime.now().strftime('%H:%M')


def waitToSomeTime(days, hours, miniutes, seconds):
    tomorrow = datetime.replace(datetime.now() + timedelta(days=days),
             hour=hours, minute=miniutes, second=seconds)
    delta = tomorrow - datetime.now()
    time.sleep(delta.seconds)

def getTickDataAAA(startTime, endTime):
    # 启动多线程获取tick数据
    for stockId in stockIDList[0:2]:
        timeArray = time.strptime(startTime, '%H:%M')
        t = threading.Thread(target=getTickData, args=(stockId, timeArray.tm_hour, timeArray.tm_min, endTime))
        t.start()

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
# stockIDList.append()

getTickDataAAA('08:50','09:40')
getTickDataAAA('11:20','11:40')
getTickDataAAA('12:55',"13:05")
getTickDataAAA('14:55',"15:05")