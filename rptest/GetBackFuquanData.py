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
    allStockList = []
    # http://vip.newapi.wmcloud-stg.com/api/equity/getEqu.json?equTypeCD=A&listStatusCD=L,S
    response = requests.get('http://vip.newapi.wmcloud-stg.com/api/equity/getEqu.json?equTypeCD=%s&listStatusCD=S' % type)
    responseContent = response.content
    jsonpathExpression = parse('$.data[*].ticker')
    for match in jsonpathExpression.find(json.loads(responseContent)):
        allStockList.append(match.value)
    return allStockList

def getTickData(stockId, hour, minute, endTime):
    while True:
        print stockId
        # 当前时间比期望监测时间晚，则从下一天开始监测
        plusDay = 0
        if datetime.now().hour == hour and datetime.now().minute > minute:
            plusDay = 1
        if datetime.now().hour > hour:
            plusDay = 1
        waitToSomeTime(plusDay, hour, minute, 0)
        print 'from %s:%s to %s' % (hour, minute, endTime)
        lastVolumn = -1
        # 当前时间
        now = datetime.now()
        startDate = now + timedelta(-5)
        startDate = startDate.strftime('%Y%m%d')
        nowDate = now.strftime('%Y%m%d')
        folderName = 'd://houfuquan//%s' % nowDate
        if not os.path.exists(folderName):
            os.mkdir(folderName, 07777)
        fileName = '%s//%s-%s.csv' % (folderName, stockId, endTime.replace(':', ''))
        csvFile = file(fileName, 'wb')
        writer = csv.writer(csvFile)
        writer.writerow(['recordTime', 'tradeDate', 'closePrice', 'marketValue'])
        csvFile.close()
        nowTime = datetime.now().strftime('%H:%M')
        lastClosePrice = 0
        while str(endTime) != str(nowTime):
            response = requests.get('https://gw.wmcloud-stg.com/rrpqa/web/stock/getStockInfoByTimeDuration?ticker=%s'
                                    '&beginDate=%s&endDate=%s&adjustType=2' % (stockId, startDate, nowDate), headers = headers)
            responseContent = response.content
            nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tradeDate = parse('$.data[*].tradeDate').find(json.loads(responseContent))[-1].value
            closePrice = parse('$.data[*].closePrice').find(json.loads(responseContent))[-1].value
            marketValue = parse('$.data[*].marketValue').find(json.loads(responseContent))[-1].value
            if lastClosePrice != closePrice:
                csvFile = open(fileName, 'a+')
                writer = csv.writer(csvFile)
                writer.writerow([nowTime, tradeDate, closePrice, marketValue])
                csvFile.close()
            lastClosePrice = closePrice
            sleep(1)
            nowTime = datetime.now().strftime('%H:%M')


def waitToSomeTime(days, hours, miniutes, seconds):
    tomorrow = datetime.replace(datetime.now() + timedelta(days=days),
             hour=hours, minute=miniutes, second=seconds)
    delta = tomorrow - datetime.now()
    time.sleep(delta.seconds)

def getTickDataAAA(startTime, endTime):
    # 启动多线程获取tick数据
    for stockId in stockIDList:
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

# # 新上市股票
# stockIDList.append('002803')
# stockIDList.append('300520')
# # 停牌股票
# stockIDList.append('600189')
# stockIDList.append('600580')
# # 正常股票
# stockIDList.append('600820')
# stockIDList.append('000783')

def getStockTestdata():
    from classtest import ReadPageSrc
    # 每天8:55分更新stockList
    hour = 8
    minute = 55
    # while True:
    # plusDay = 0
    # if datetime.now().hour == hour and datetime.now().minute > minute:
    #     plusDay = 1
    # if datetime.now().hour > hour:
    #     plusDay = 1
    # waitToSomeTime(plusDay, hour, minute, 0)
    allStockList = getStockList('A')
    webPage = ReadPageSrc.WebPage('http://stock.10jqka.com.cn/hstp_list/')
    matchList = webPage.getContentByReg('<a target="_blank" title="沪市今日停牌一览.*?" href="(.*?shtml)">沪市今日停牌一览.*?</a>')
    url = matchList[0]
    webPage = ReadPageSrc.WebPage(url)
    print url
    stoppedStockList = webPage.getContentByReg('<td style="border-color:#000000;font-size:12px;line-height:normal;">(\d+)</td>')

    webPage = ReadPageSrc.WebPage('http://www.chaguwang.cn/zixun/newstock.php')
    newStockList = webPage.testBeautifulSoup()
    global stockIDList
    stockIDList = []
    stockIDList.extend(newStockList[0:3])
    stockIDList.extend(stoppedStockList[0:3])
    stockIDList.extend(allStockList[0:3])
    print stockIDList

getStockTestdata()
getTickDataAAA('09:19','09:40')
getTickDataAAA('11:20','11:40')
getTickDataAAA('12:55',"13:05")
getTickDataAAA('14:55',"15:05")