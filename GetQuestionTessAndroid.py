# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : 答题闯关辅助，截屏 ，OCR 识别，百度搜索


from PIL import Image
from common import screenshot, ocr, methods
from threading import Thread
import time
import tkinter as tk
from win32api import GetSystemMetrics
from queue import Queue
import requests
import time
import sys
import os

global GUI
global running
running = True
GUI = False
argv = sys.argv;
if (len(argv)>1 and argv[1]=='gui'):
    GUI = True;

if GUI:
    top = tk.Tk()
    top.geometry(str(int(GetSystemMetrics(0)/2))+'x'+str(int(GetSystemMetrics(1)/2)))

def hit_me():
    global GUI
    global running
    global touch_start
    global save_choices
    # 截图
    # screenshot.check_screenshot()

    img = Image.open("./screenshot.png")

    # 文字识别
    question, choices, selection_start = ocr.ocr_img(img)
    touch_start = selection_start
    save_choices = choices

    result = '问题：'+question+'\n\n';

    for choice in choices:
        result += choice + '\n'

    if GUI:
        var.set(result)   # 设置标签的文字为 'you hit me'

    # t = time.clock()
    # 用不同方法输出结果，取消某个方法在前面加上#

    # # 打开浏览器方法搜索问题
    # methods.run_algorithm(0, question, choices)
    # # 将问题与选项一起搜索方法，并获取搜索到的结果数目
    # methods.run_algorithm(1, question, choices)
    # # 用选项在问题页面中计数出现词频方法
    # methods.run_algorithm(2, question, choices)

    # 多线程
    q = Queue()
    
    m1 = Thread(methods.run_algorithm(0, question, choices, q))
    m2 = Thread(methods.run_algorithm(1, question, choices, q))
    m3 = Thread(methods.run_algorithm(2, question, choices, q))
    m4 = Thread(methods.run_algorithm(3, question, choices, q))
    m1.start()
    m2.start()
    m3.start()
    m4.start()

    global sum
    global paramsQuestion
    global paramsAnswer
    global results
    results = {
        'cloud_count':'',
        'open_webbrowser_count':'',
        'count_base':''
    }

    paramsQuestion = question
    paramsAnswer = ''
    sum=0
    def consumer(in_q):
        global touch_start
        global GUI
        global sum
        global paramsQuestion
        global paramsAnswer
        global results
        global save_choices
        while True:
            data = in_q.get()
            if (data == 'END'):
                sum = sum + 1
            else:
                if GUI:
                    results[data['name']]=data['value'];
            if (sum>2):
                break
        if (results['cloud_count']!=''):
            paramsAnswer = results['cloud_count']
        elif (results['count_base']!=''):
            paramsAnswer = results['count_base']
        elif (results['open_webbrowser_count']!=''):
            paramsAnswer = results['open_webbrowser_count']
        else:
            paramsAnswer = '自求多福'


        selection = 0
        for index, item in enumerate(save_choices):
            if item==paramsAnswer:
                selection = index
                break

        selection_height = 170;

        if GUI:
            var.set(var.get() + '\n\n正确答案\n\n' +paramsAnswer)
            # 模拟点按

        os.system('adb shell input tap 250 ' + str(touch_start+(selection+1)*selection_height/2))

        req = requests.get(url='http://localhost:3000/add', params={'question': paramsQuestion, 'answer': paramsAnswer})

    t = Thread(target=consumer, args=(q,))
    t.start()
    if (GUI==False):
        go = input('输入回车继续运行,输入 n 回车结束运行: ')
        if go == 'n':
            running = False

        print('------------------------')

if GUI:
    b = tk.Button(top, 
        text='开始',      # 显示在按钮上的文字
        width=15, height=2, 
        command=hit_me)     # 点击按钮式执行的命令
    b.pack()    # 按钮位置
    var = tk.StringVar()    # 这时文字变量储存器
    l = tk.Label(top, 
        textvariable=var,   # 使用 textvariable 替换 text, 因为这个可以变化
        bg='#DDDDDD', font=('微软雅黑', 12), width=int(GetSystemMetrics(0)/2), height=int(GetSystemMetrics(1)/2)-2)
    l.pack() 
    # 进入消息循环
    top.mainloop()
else:
    while running:
        hit_me()


