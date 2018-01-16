# -*- coding:utf-8 -*-
import urllib
import requests
from lxml import etree

def spider_label():
    url = "http://www.lizhi.fm/promo/"
    response = requests.get(url).text
    html = etree.HTML(response)
    label_ids = html.xpath('//div[2]/div[2]/div/ul/li/a/@href')
    label_names = html.xpath('//div[2]/div[2]/div/ul/li/a/text()')
    for (label_id,label_name) in zip(label_ids,label_names):
        # print label_id
        # print label_name
        if label_id == "/label/24229822051386544/":
            label_name = "rock"
            # print '1111111111111111'
            # print label_name
            # print label_id
        elif label_id=="/label/24229824198870320/":
            label_name ="ballad"
            # print '222222222222222222'
            # print label_name
            # print label_id
        elif label_id=="/label/24229826346354096/":
            label_name = 'dianyin'
            # print '3333333333333333333'
            # print label_name
            # print label_id
        elif label_id == "/label/24229829567579696/":
            label_name = "absolute_music"
            # print '44444444444444444'
            # print label_name
            # print label_id
        elif label_id=='/label/24229832251934384/':
            label_name='cover_version'
            # print '5555555555555'
            # print label_name
            # print label_id
        else:
            label_name='fashion '
            # print '66666666666666'
            # print label_name
            # print label_id

        get_spider(label_id,label_name)

def get_spider(label_id,label_name):
    print label_id
    print label_name
    print '11111111111111'



if __name__ == '__main__':
    spider_label()
#
# u = '//www.lizhi.fm/user/2604453434516522028'
# h = "http:"+u
# print h