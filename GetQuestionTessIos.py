# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : 答题闯关辅助，截屏 ，OCR 识别，百度搜索

import wda
from PIL import Image
from common import  ocr, methods
import os
import pytesseract
import webbrowser

c = wda.Client()

# 截图
c.screenshot('screenshot.png')

img = Image.open("./screenshot.png")

# 文字识别
question, choices = ocr.ocr_img(img)

# 用不同方法输出结果

# 打开浏览器方法搜索问题
methods.run_algorithm(0, question, choices)
# 将问题与选项一起搜索方法，并获取搜索到的结果数目
methods.run_algorithm(1, question, choices)
# 用选项在问题页面中计数出现词频方法
methods.run_algorithm(2, question, choices)