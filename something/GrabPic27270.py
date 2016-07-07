#coding=utf-8

import re
import urllib2
import sys
import os
import shutil
# import chardet


def getHtml(url):
    content = urllib2.urlopen(url).read()
    type = sys.getfilesystemencoding()
    # print type
    content = content.decode("gb2312","ignore").encode("utf-8")
    # print content
    return content

def getImg(url, wholeUrlList):
    #进入一个页面 先下载主要图片 后获取所有的url 存入一个list中 去重
    #再去遍历这个list 这个list会越来越大 然后越来越小

    tempurl = url[0:len(url)-5] + "_%d" + ".html"

    reg = r'.*?/(\d+).html'
    foldername = re.compile(reg).findall(url)
    path = "D:\\pythontest\\" + foldername[0]
    print path
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path, 07777)
    os.chdir(path)
    os.getcwd()

    for x in range(0, 10):
        try:
            print("page url is " + tempurl % x)
            html = getHtml(tempurl % x)
            urlreg = r'<a href="(http://www.27270.com/ent/meinvtupian.+?\d+?.html)"'
            imgUlrList = re.compile(urlreg).findall(html)
            wholeUrlList = list(set(imgUlrList + wholeUrlList))
            imgreg = r'img alt=".+?"\s+src=(.+?.jpg)'
            imgList = re.compile(imgreg).findall(html)
            imgurl = imgList[0]
            imgurl = imgurl[1:len(imgurl)]
            print "img url is " + imgurl
            picname = "%d.jpg" % x
            conn = urllib2.urlopen(imgurl)
            f = open(picname, "wb")
            f.write(conn.read())
            f.close()
            x = x + 1
        except:
            if x>10:
                break
            else:
                continue
    return wholeUrlList


wholeUrlList = ["http://www.27270.com/ent/meinvtupian/2016/154928.html"]
# for x in range(2001, 2010):
# getImg("http://www.2cto.com/meinv/rhmeinv/%d.html" % x, wholeUrlList)
# for url in wholeUrlList:
#     wholeUrlList = getImg(url, wholeUrlList)
#     print "aaa"

while len(wholeUrlList) > 0:
    url = wholeUrlList.pop(0)
    wholeUrlList = getImg(url, wholeUrlList)
    print "aaa"

