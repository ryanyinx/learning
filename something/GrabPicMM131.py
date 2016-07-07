#coding=utf-8

import re
import urllib2
import sys
import os
# import chardet

def getHtml(url):
    content = urllib2.urlopen(url).read()
    type = sys.getfilesystemencoding()
    print type
    content = content.decode("gb2312").encode(type)
    # print content
    return content

def getImg(html):
    reg = r'<img alt=.*\s+src="(.+?)\d\.jpg"'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)
    imgurl = imglist[0]
    reg = r'.*?pic/(\d+)/'
    foldername = re.compile(reg).findall(imgurl)
    path = "/Users/Ryan/Pictures/" + foldername[0]
    print path
    if os.path.exists(path):
        os.rmdir(path)
    os.mkdir(path, 07777)
    os.chdir(path)
    os.getcwd()
    for x in range(1,200):
        try:
            print imgurl
            picname = "%d.jpg" % x
            url = imgurl+picname
            print url
            conn = urllib2.urlopen(url)
            f = open(picname, "wb")
            f.write(conn.read())
            f.close()
            x = x + 1
        except:
            break

for x in range(2500,2600):
    try:
        html = getHtml("http://www.mm131.com/xinggan/%d.html" % x)
        getImg(html)
    except:
        continue