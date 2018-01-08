# -*- coding: utf-8 -*-

# @Author  : livc 链接：https://livc.io/blog/204
# @Time    : 2018/1/8 21:36

# python3
#import wda
import io
import urllib.parse
import webbrowser
import requests
import time
import base64
from PIL import Image

c = wda.Client()
# 百度OCR API
api_key = ''
api_secret = ''
token = ''


while True:
    time.sleep(0.5)
    c.screenshot('1.png')
    im = Image.open("./1.png")
    region = im.crop((75, 315, 1167, 789)) # iPhone 7P
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
    break

