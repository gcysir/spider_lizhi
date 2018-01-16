# -*- coding:utf-8 -*-
import re
import requests
import urllib
from lxml import etree

def spider_rock():
    number = 1
    while True:
        url = "http://www.lizhi.fm/label/24412443792375856/"+str(number)+".html"
        response = requests.get(url).content
        html = etree.HTML(response)
        list_url = html.xpath('//ul/li/p[1]/a/@href')
        number += 1

        for i in list_url:
            h = "http:"+i
            print h
        print len(list_url)
        print list_url
        if len(list_url)<24:
            break

if __name__ == '__main__':
    spider_rock()