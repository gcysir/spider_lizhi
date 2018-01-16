# -*- coding:utf-8 -*-
import requests
import re
from lxml import etree

def spider_info():
    url = "http://www.lizhi.fm/user/2604453434516522028"
    response = requests.get(url).content
    html = etree.HTML(response)
    user_info_name = html.xpath('//div[2]/div[3]/div[2]/h1/text()')[0]
    user = re.split(' ',user_info_name)
    fm = user[0]
    name = user[1]
    print fm
    print name
    print user_info_name
if __name__ == '__main__':
    spider_info()