# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : 答题闯关辅助，截屏 ，OCR 识别，百度搜索


from PIL import Image
from common import screenshot, ocr, methods
from threading import Thread
import time
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('./config/configure.conf', encoding='utf-8')


while True:
    # 截图
    t = time.clock()
    screenshot.check_screenshot()

    #end_time = time.clock()
    #print(end_time - t)

    img = Image.open("./screenshot.png")

    # 文字识别,可选 Tesseract 和 Baidu ,请在 orc.py 中进行相应配置

    #ocr_img: 需要分别截取题目和选项区域，使用 Tesseract
    #ocr_img_tess： 题目和选项一起截，使用 Tesseract
    #ocr_img_baidu： 题目和选项一起截，使用 baidu ocr，需配置 key
    
    # question, choices = ocr.ocr_img(img, config)
    question, choices = ocr.ocr_img_tess(img, config)
    # question, choices = ocr.ocr_img_baidu(img, config)

    #end_time2 = time.clock()
    #print(end_time2 - end_time)

    # 用不同方法输出结果，取消某个方法在前面加上#

    # # 打开浏览器方法搜索问题
    # methods.run_algorithm(0, question, choices)
    # # 将问题与选项一起搜索方法，并获取搜索到的结果数目
    # methods.run_algorithm(1, question, choices)
    # # 用选项在问题页面中计数出现词频方法
    # methods.run_algorithm(2, question, choices)

    # 多线程
    m1 = Thread(methods.run_algorithm(0, question, choices))
    m2 = Thread(methods.run_algorithm(1, question, choices))
    m3 = Thread(methods.run_algorithm(2, question, choices))
    m1.start()
    m2.start()
    m3.start()

    end_time3 = time.clock()
    print('用时: {0}'.format(end_time3 - t))

    go = input('输入回车继续运行,输入 n 回车结束运行: ')
    if go == 'n':
        break

    print('------------------------')
