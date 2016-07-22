#coding=utf-8

import re
import urllib2
import sys
import os
import shutil
# import chardet
from sgmllib import SGMLParser
from bs4 import BeautifulSoup

class ListNaem(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)


class WebPage():
    def __init__(self, url):
        self.url = url
        self.getHtml()

    def getHtml(self):
        self.page = urllib2.urlopen(self.url)
        content = urllib2.urlopen(self.url).read()
        # type = sys.getfilesystemencoding()
        content = content.decode("gb2312","ignore").encode("utf-8")
        self.pageSrc = content

    def getContentByReg(self, reg):
        reg = r'%s' % reg
        resultList = re.compile(reg).findall(self.pageSrc)
        return resultList

    # only suitable for http://www.chaguwang.cn/zixun/newstock.php
    def testBeautifulSoup(self):
        # BeautifulSoup(open('index.html'))
        newStockList = []
        soup = BeautifulSoup(self.page, 'lxml')
        # print soup.prettify()
        indexOfTradeDate = 0
        for child in soup.table.contents:
            try:
                index = 0
                if indexOfTradeDate == 0:
                    for aaa in child.contents:
                        if aaa.string == u'上市日期':
                            indexOfTradeDate = index
                            break
                        index+=1
                else:
                    tradeDate = child.contents[indexOfTradeDate]
                    if not (tradeDate.string == u'\xa0' or tradeDate.string is None):
                        newStockList.append(child.contents[1].string)
            except:
                a = 0
        return newStockList
webPage = WebPage('http://stock.10jqka.com.cn/hstp_list/')
matchList = webPage.getContentByReg('<a target="_blank" title="沪市今日停牌一览.*?" href="(.*?shtml)">沪市今日停牌一览.*?</a>')
url = matchList[0]
webPage = WebPage(url)
print url
stoppedStockList = webPage.getContentByReg('<td style="border-color:#000000;font-size:12px;line-height:normal;">(\d*)</td>')

webPage = WebPage('http://www.chaguwang.cn/zixun/newstock.php')
newStockList = webPage.testBeautifulSoup()