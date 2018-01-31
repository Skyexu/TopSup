# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : 答题闯关辅助，截屏 ，OCR 识别，百度搜索


from PIL import Image
from common import screenshot, ocr, methods
from threading import Thread
import time

import requests
import time
import sys
import os
import random

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

global platform
from colorama import init,Fore
init()


GUI = False
AUTO = True

global count
count = 0

def hit_me():
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
    global platform
    getMax=False

    token = '88QUg$!pmf!TAY5r';

    if platform=='auto':
        go = input('输入回车运行,输入 n 回车结束运行: ')
        if go == 'n':
            return
    # 截图
    screenshot.check_screenshot()

    img = Image.open("./screenshot.png")

    # 文字识别
    question, choices, selection_start = ocr.ocr_img(img, platform)

    if (count > 100):
        print('退出')
        return

    if (question=='' or len(choices)==0 or selection_start==0):
        status = 'waiting'
        print('未检测到题板')
        count = count + 1
        print('休息1s')
        time.sleep(1)
        return hit_me()
    #     if running:
    #         return hit_me()

    containSum = 0
    for q in question:
        if (q.index(current_question)>-1):
            containSum = containSum + 1

    if (containSum*100/len(question)>80):
        if (status != 'waiting'):
            print('此题已答过')
            print('休息5s')
            time.sleep(5)
            return hit_me()
    #         if running:
    #             return hit_me()
        if (touch_start==-1):
            return hit_me()
        current_answer = ocr.get_question(img, touch_start, platform)
        if (current_answer < len(answers)):
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
        return output(choices, counts,'count_base', question)

    def open_webbrowser_count(question,choices):
        global getMax
        print('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
        # q.put('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
        print('Question: ' + question)
        if ('不' in question or '错误' in question):
            getMax = False
            print('**请注意此题为否定题,选计数最少的**')
        else:
            getMax = True

        counts = []
        for i in range(len(choices)):
            # 请求
            req = requests.get(url='http://www.baidu.com/s', params={'wd': question + choices[i]})
            content = req.text
            index = content.find('百度为您找到相关结果约') + 11
            content = content[index:]
            index = content.find('个')
            count = content[:index].replace(',', '')
            counts.append(count)
        return output(choices, counts, 'open_webbrowser_count', question)

    def output(choices, counts, al_num, question):
        global getMax
        if (len(counts)==0):
            return random.choice([0,1,2]);
        counts = list(map(int, counts))

        # 计数最高
        index_max = counts.index(max(counts))

        # 计数最少
        index_min = counts.index(min(counts))

        if index_max == index_min:
            print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
            if al_num=='count_base':
                return open_webbrowser_count(question, choices)
            else:
                return random.choice([0,1,2])

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

    if (len(choices) <3 or selection>2):
        return hit_me();
    print('\n我要选'+choices[selection])
    if (platform=='zs'):
        #芝士超人
        answer_height = 200
    elif (platform=='hj' or platform =='cd'):
        #花椒直播
        # 冲顶大会
        answer_height = 150

    if (platform!='auto'):
        os.system('adb shell input tap 250 ' + str(touch_start+(selection+0.5)*answer_height))
    # if running:
    #     hit_me()
    req   = requests.get(url='http://hj.chenzhicheng.com/', params={'advise': selection, 'token':token})
    print(req.text)
    print('休息5s')
    time.sleep(5)
    return hit_me()


go = input('请选择平台：\n1. 芝士超人\n2. 花椒直播 \n3. 冲顶大会 \n4. 普遍适应\n')
if go=='1':
    platform = 'zs'
elif go=='2':
    platform = 'hj'
elif go=='3':
    platform = 'cd'
elif go=='4':
    platform = 'auto'
# while running:
hit_me()