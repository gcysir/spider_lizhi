# -*- coding:utf-8 -*-
import re
import urllib
import requests
import os

def get_img(file_path="img"):
    img = "http://cdnimg103.lizhi.fm/user/2015/04/21/19499578363219202_160x160.jpg"
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
get_img()