# -*- coding:utf-8 -*-
# @Time     :2018-01-15
# @Author   :gcy
# @Email    :
# @File     :
import requests
import sys
import re
import os
import pymongo
import urllib
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import choice
reload(sys)
sys.setdefaultencoding('utf-8')
ua_list = UserAgent()

proxy_list = []
def get_ip(numpage):
    '''获取代理IP'''
    for num in xrange(1, numpage + 1):
        url = "http://www.xicidaili.com/wn/"
        # url = 'http://www.xicidaili.com/nn'
        my_headers = {
            'Accept': 'text/html, application/xhtml+xml, application/xml;',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'http: // www.xicidaili.com/nn',
            "User-Agent": ua_list.random
        }
        r = requests.get(url,headers=my_headers)
        soup = BeautifulSoup(r.text,'html.parser')
        data = soup.find_all('td')

        #定义IP和端口Pattern规则
        ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  #匹配IP
        port_compile = re.compile(r'<td>(\d+)</td>')  #匹配端口
        ips = re.findall(ip_compile,str(data))    #获取所有IP
        ports = re.findall(port_compile,str(data))  #获取所有端口
        # z = [':'.join(i) for i in zip(ip,port)]  #列表生成式
        for (ip,port) in zip(ips,ports):
            ip = ''.join(ip)+":"+''.join(port)
            http={"https": 'https://' + ip}
            url="http://ip.chinaz.com/getip.aspx"
            try:
                response = requests.get(url,proxies=http)
            except Exception,e:
                print e
            else:
                proxy_list.append(ip)
                print ip
    main()

def main():
    url = "http://www.lizhi.fm/promo/"
    response = requests.get(url).text
    html = etree.HTML(response)
    label_ids = html.xpath('//div[2]/div[2]/div/ul/li/a/@href')
    label_names = html.xpath('//div[2]/div[2]/div/ul/li/a/text()')
    for (label_id, label_name) in zip(label_ids, label_names):
        print label_id
        print label_name
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
        spider_rock(label_id, label_name)



def spider_rock(label_id,label_name):
    number = 1
    while True:
        header = {

            "User-Agent": ua_list.random
        }
        ip = choice(proxy_list)
        http = {"https": 'https://' + ip}
        url = "http://www.lizhi.fm"+label_id+ str(number) + ".html"
        response = requests.get(url, headers=header, proxies=http).content
        html = etree.HTML(response)
        list_url = html.xpath('//ul/li/p[1]/a/@href')
        number += 1
        for i in list_url:
            user_url = "http:"+i
            spider_info(user_url,label_name)
        if len(list_url)<24:
            break


def spider_info(user_url,label_name,file_path="lizhiImg"):
    header = {
        "User-Agent": ua_list.random
    }
    ip = choice(proxy_list)
    http = {"https": 'https://' + ip}
    response = requests.get(user_url,headers=header, proxies=http).content
    html = etree.HTML(response)
    user_info_name = html.xpath('//div[2]/div[3]/div[2]/h1/text()')[0]
    user = re.split(' ', user_info_name)
    fm = user[0]
    name = re.search(r'\s(.*)', user_info_name).group(1)
    audio = html.xpath('//div[1]/p[1]/span[1]/text()')[0]
    play = html.xpath('//div[1]/p[1]/span[2]/text()')[0]
    fans = html.xpath('//div[1]/p[1]/span[3]/text()')[0]
    tag = html.xpath('//div[3]/div[2]/div[1]/div/a/text()')
    radio = html.xpath('//div[2]/div[1]/p[2]/span/text()')
    signature = html.xpath('//div[3]/div[2]/div[2]/text()')[0]
    img = html.xpath('//div[2]/div[3]/div[1]/img/@src')[0]
    img1 = re.match(r'(.*)_',img).group()
    img2 = ''.join(re.findall(r'_160x160(.*)',img))
    big_img = img1 + "834x834" + img2
    center_img = img1 + "188x188" + img2
    small_img = img1 + "142x142" + img2
    # 保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        if not os.path.exists(file_path):
            print '文件夹', file_path, '不存在，重新建立'
            # os.mkdir(file_path)
            os.makedirs(file_path)
        file_suffix = ''.join(re.findall(r'fm(.*)', img)).split('/')[-1]  # 本地路径
        print file_suffix
        # 拼接图片名（包含路径）
        filename = '{}{}{}'.format(file_path, os.sep, file_suffix)
        # 下载图片，并保存到文件夹中
        # filename =
        urllib.urlretrieve(img, filename=filename)
    except IOError as e:
        print '文件操作失败', e
    except Exception as e:
        print '错误 ：', e

    # print big_img
    # print center_img
    # print small_img
    # print fm
    # print name
    # print user_info_name
    # print audio
    # print play
    # print fans
    # print tag
    # print radio
    # print signature
    # print img
    data1={
        "big_img":big_img,
        "center_img":center_img,
        "small_img":small_img,
        "img": img,
        "fm":fm,
        "name":name,
        "user_info_name":user_info_name,
        "audio":audio,
        "play":play,
        "fans":fans,
        "tag":''.join(tag),
        "radio":''.join(radio),
        "signature":signature,
    }
    list_id = html.xpath('//div[2]/div[6]/ul/li/a/@href')
    spider_song_info(list_id,data1,fm,label_name)


def spider_song_info(list_id,data1,fm,label_name):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['lizhimusic']
    list = []
    print '专辑列表开始爬取。。。。。。。。。。。。。。。。。'
    for id in list_id:
        song_url = "http://www.lizhi.fm"+id
        header = {
            "User-Agent": ua_list.random
        }
        ip = choice(proxy_list)
        http = {"https": 'https://' + ip}
        response = requests.get(song_url,headers=header, proxies=http).content
        html = etree.HTML(response)
        audioName = ''.join(html.xpath('//div[1]/div/div[2]/h1/text()'))
        audioDate2 = html.xpath('//div/div[2]/p[1]/span[1]/text()')
        audioDate1 =''.join(audioDate2)
        a = re.compile('-')
        audioDate= a.sub('/', audioDate1)
        audioId = ''.join(html.xpath('//div[1]/div/div[2]/div/div[2]/@data-id'))
        audioMp3 = "http://cdn5.lizhi.fm/audio/"+audioDate+"/"+audioId+"_hd.mp3"
        audioTimes = ''.join(html.xpath('//div[2]/p[1]/span[2]/text()'))
        audioUser = ''.join(html.xpath('//div[1]/div/div[2]/p[2]/span/a/text()'))
        audioPlay = ''.join(html.xpath('//div/div[2]/p[3]/span[1]/text()'))
        audioDownloadNumber = ''.join(html.xpath('//div[1]/div/div[2]/p[3]/span[2]/text()'))
        audioImg = ''.join(html.xpath('//div[2]/div[3]/div[1]/div/div[1]/img/@src'))
        # img1 = re.match(r'(.*)_', audioImg).group()
        img1 = ''.join(re.findall(r'(.*)_',audioImg))
        img2 = ''.join(re.findall(r'_320x320(.*)', audioImg))
        big_audioImg = img1 +"_"+ "834x834" + img2
        center_audioImg = img1+"_" + "188x188" + img2
        small_audioImg = img1 +"_"+ "142x142" + img2
        print audioName
        print audioDate
        print audioId
        print audioTimes
        print audioUser
        print audioPlay
        print audioDownloadNumber
        print big_audioImg
        print center_audioImg
        print small_audioImg
        print audioMp3
        data2= {
            "audioName":audioName,
            "audioDate":audioDate,
            "audioId":audioId,
            "audioTimes":audioTimes,
            "audioMp3":audioMp3,
            "audioUser":audioUser,
            "audioPlay":audioPlay,
            "audioDownload":audioDownloadNumber,
            "big_audioImg":big_audioImg,
            "center_audioImg":center_audioImg,
            "small_audioImg":small_audioImg
        }

        if len(audioDate2)==0:
            continue
        else:
            list.append(data2)
        msg2 = db[label_name+'_list']
        msg2.insert_one(data2)
    msg1 = db[label_name+'_header']
    msg3 = db[label_name+'_info']
    msg1.insert_one(data1)
    dict = {
        'fm':fm,
        "header_info":data1,
        "list_info":list
    }
    msg3.insert(dict)
    print '专辑列表存储成功。。。。。。。。。。。。。。。。。'
    if len(list) < 1:
        idm = str(fm)
        id3 = db[label_name+'_header'].find_one({'fm':idm})['_id']
        id4 = db[label_name+'_info'].find_one({'fm': idm})['_id']
        db[label_name + '_header'].remove(id3)
        db[label_name + '_info'].remove(id4)



if __name__ == '__main__':
    get_ip(1)