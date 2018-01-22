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
import random

global GUI
global AUTO
global current_question
current_question = ''
global answers
answers = []
global current_answer
current_answer = ''
global current_bigData
current_bigData = 0

global running
running = True

global status
status = 'waiting'

global touch_start
from colorama import init,Fore
init()


GUI = False
AUTO = True
argv = sys.argv;
if (len(argv)>1 and argv[1]=='gui'):
    GUI = True;

if GUI:
    top = tk.Tk()
    top.geometry(str(int(GetSystemMetrics(0)/2))+'x'+str(int(GetSystemMetrics(1)/2)))

global count
count = 0

def hit_me():
    global GUI
    global running
    global touch_start
    global save_choices
    global AUTO
    global current_question
    global answers
    global current_answer
    global current_bigData
    global status
    global count
    global getMax
    getMax=False

    token = '88QUg$!pmf!TAY5r';

    # 截图
    screenshot.check_screenshot()

    img = Image.open("./screenshot.png")

    # 文字识别
    question, choices, selection_start = ocr.ocr_img(img)

    print(status)
    print(count)

    if (count > 100):
        print('退出')
        return

    if (question=='' or len(choices)==0 or selection_start==0):
        status = 'waiting'
        print('未检测到题板')
        count = count + 1
        return hit_me()
    #     if running:
    #         return hit_me()

    if (question == current_question or (question in current_question)):
        if (status != 'waiting'):
            print('此题已答过')
            return hit_me()
    #         if running:
    #             return hit_me()
        current_answer = ocr.get_question(img, touch_start)
        print('正确答案为：'+answers[current_answer])
        # req = requests.get(url='http://localhost:3000/add', params={'question': current_question, 'answer': answers[current_answer], 'bigdata':answers[current_bigData]})
        # print(req)
        req   = requests.get(url='http://hj.chenzhicheng.com/', params={'right': current_answer, 'token':token})
        print(req.text)
        return hit_me()

    #     if running:
    #         return hit_me()
    count = 0
    status = 'answered'
    req   = requests.get(url='http://hj.chenzhicheng.com/', params={'question': question, 'answer': choices, 'token':token})
    print(req.text)

    current_question = question
    answers = choices

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
    # methods.run_algorithm(2, question, choices, q)

    def count_base(question,choices):
        global getMax
        print('\n-- 方法3： 题目搜索结果包含选项词频计数法 --\n')
        # q.put('\n-- 方法3： 题目搜索结果包含选项词频计数法 --\n')
        # 请求
        req = requests.get(url='http://www.baidu.com/s', params={'wd':question})
        content = req.text
        #print(content)
        counts = []
        print('Question: '+question)
        if ('不' in question or '错误' in question):
            print('**请注意此题为否定题,选计数最少的**')
            getMax = False
        else:
            getMax = True

        for i in range(len(choices)):
            counts.append(content.count(choices[i]))
            #print(choices[i] + " : " + str(counts[i]))
        return output(choices, counts,'count_base')

    def output(choices, counts, al_num):
        global getMax
        if (len(counts)==0):
            return random.choice([0,1,2]);
        counts = list(map(int, counts))
        #print(choices, counts)

        # 计数最高
        index_max = counts.index(max(counts))

        # 计数最少
        index_min = counts.index(min(counts))

        if index_max == index_min:
            print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
            return random.choice([0,1,2]);

        result = 0;
        for i in range(len(choices)):
            if i == index_max:
                # 绿色为计数最高的答案
                print(Fore.GREEN + "{0} : {1} ".format(choices[i], counts[i]) + Fore.RESET)
                if getMax:
                    result=i

            elif i == index_min:
                # 红色为计数最低的答案
                print(Fore.MAGENTA + "{0} : {1}".format(choices[i], counts[i]) + Fore.RESET)
                if (getMax==False):
                    result=i

            else:
                print("{0} : {1}".format(choices[i], counts[i]))
                # q.put(' '+str(choices[i]) + ':' + str(counts[i]) + '\n')
        return result

    selection = count_base(question, choices)

    print(choices)
    print('\n我要选'+choices[selection])
    platform='cd'
    if (platform=='zs'):
        #芝士超人
        answer_height = 100
    elif (platform=='hj' or platform =='cd'):
        #花椒直播
        # 冲顶大会
        answer_height = 150

    print(touch_start+(selection+0.5)*answer_height)
    os.system('adb shell input tap 250 ' + str(touch_start+(selection+0.5)*answer_height))
    # if running:
    #     hit_me()
    req   = requests.get(url='http://hj.chenzhicheng.com/', params={'advise': selection, 'token':token})
    print('休息5s')
    time.sleep(5)
    print('休息结束')
    print(req.text)
    return hit_me()

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
        global status

        while True:
            data = in_q.get()
            if (data == 'END'):
                sum = sum + 1
            else:
                results[data['name']]=data['value']
            if (sum>2):
                break

        if (sum>2):
            print(results)
            # if (results['cloud_count']!=''):
            #     paramsAnswer = results['cloud_count']
            if (results['count_base']!=''):
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

            if  (paramsAnswer=='自求多福'):
                selection = random.choice([0,1,2]);

            selection_height = 170;

            if GUI:
                var.set(var.get() + '\n\n正确答案\n\n' +paramsAnswer)
                # 模拟点按

            current_bigData = selection
            print('\n我要选'+paramsAnswer)
            os.system('adb shell input tap 250 ' + str(touch_start+(selection+0.5)*selection_height))
            # if running:
            #     hit_me()
            print('休息5s')
            time.sleep(5)
            print('休息结束')
            hit_me()

    t = Thread(target=consumer, args=(q,))

    if (count==1):
        t.start()
    if (GUI==False and AUTO==False):
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