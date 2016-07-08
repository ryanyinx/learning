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

def getPriceRequest():
    r = requests.get('https://gw.wmcloud.com/ira/mobile/whitelist'
                     '/stock/ticker?type=1&tickers=000001,000002,600000,600006,000423',
                      headers={'Content-Type': 'application/json'})
    return r.json()

def printlog(data):
    # del data[]
    NowData = {}
    second = {}
    third = {}
    i=0
    while(i<5):
        a = data['tickRTSnapshotList']['tickRTSnapshot'][i]['shortNM']
        b = 'suspension: '+ str(data['tickRTSnapshotList']['tickRTSnapshot'][i]['suspension'])
        c = 'lastPrice: '+str(data['tickRTSnapshotList']['tickRTSnapshot'][i]['lastPrice'])
        NowData[a] = [b,c]
        i = i+1

    myfile = open('app.log', 'a')  # open for output (creates)
    myfile.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+
                 str(sorted(NowData.items(), key=lambda d:d[1], reverse = True))+'\n' )  # write a line of text
    myfile.close()
    return NowData

# sleep(1)
# i = 0
# while(i<720):
#     printlog(getPriceRequest())
#     sleep(5)
#     i = i+1
# print('success')
