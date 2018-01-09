# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    :  答题闯关辅助，截屏 ，百度 OCR 识别 api，百度搜索


import wda
import io
import urllib.parse
import webbrowser
import requests
import base64
import matplotlib.pyplot as plt
from PIL import Image
import os

c = wda.Client()

# 百度OCR API ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
api_key = ''
api_secret = ''



# 获取token
host =  'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+api_secret
headers = {
    'Content-Type':'application/json;charset=UTF-8'
}

res = requests.get(url=host,headers=headers).json()
token = res['access_token']


c.screenshot('screenshot.png')
im = Image.open("./screenshot.png")

region = img.crop((50, 350, 1000, 560)) # 坚果 pro1
#region = img.crop((75, 315, 1167, 789)) # iPhone 7P

imgByteArr = io.BytesIO()
region.save(imgByteArr, format='PNG')
image_data = imgByteArr.getvalue()
base64_data = base64.b64encode(image_data)
r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
              params={'access_token': token}, data={'image': base64_data})
result = ''
for i in r.json()['words_result']:
    result += i['words']
result = urllib.parse.quote(result)
webbrowser.open('https://baidu.com/s?wd='+result)


