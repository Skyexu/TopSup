# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser
import urllib.parse
import json
import time

# # 颜色兼容Win 10
from colorama import init,Fore
init()

global getMax
getMax = True

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

def open_webbrowser(question):
    # print("Cancel")
    # webbrowser.open('https://www.google.co.uk/search?q=' + urllib.parse.quote(question))
    # webbrowser.open('https://www.sogou.com/web?query=' + urllib.parse.quote(question))
    webbrowser.open('https://www.baidu.com/s?wd=' + urllib.parse.quote(question))

def cloud_count(question, q):
    print('\n-- 方法1： 题库筛选 --\n')
    # q.put('\n-- 方法1： 题库筛选 --\n')
    req = requests.get(url='http://localhost:3000/query', params={'question': question})
    result = json.loads(req.text, object_hook=JSONObject)
    try:
        q.put({ 'name':'cloud_count', 'value':result.answer})
        print(result.answer)
    except AttributeError as e:
        pass 
    q.put('END')

def open_webbrowser_count(question,choices,q):
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
        #print(choices[i] + " : " + count)
    output(choices, counts, q, 'open_webbrowser_count')

def count_base(question,choices,q):
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
    output(choices, counts, q, 'count_base')

def output(choices, counts, q, al_num):
    global getMax
    if (len(counts)==0):
        return
    counts = list(map(int, counts))
    #print(choices, counts)

    # 计数最高
    index_max = counts.index(max(counts))

    # 计数最少
    index_min = counts.index(min(counts))

    if index_max == index_min:
        print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        q.put('END')
        return

    for i in range(len(choices)):
        if i == index_max:
            # 绿色为计数最高的答案
            print(Fore.GREEN + "{0} : {1} ".format(choices[i], counts[i]) + Fore.RESET)
            if getMax:
                q.put({ 'name':al_num, 'value':str(choices[i])})

        elif i == index_min:
            # 红色为计数最低的答案
            print(Fore.MAGENTA + "{0} : {1}".format(choices[i], counts[i]) + Fore.RESET)
            if (getMax==False):
                q.put({ 'name':al_num, 'value':str(choices[i])})

        else:
            print("{0} : {1}".format(choices[i], counts[i]))
            # q.put(' '+str(choices[i]) + ':' + str(counts[i]) + '\n')
    q.put('END')


def run_algorithm(al_num, question, choices, q):
    if al_num == 0:
        open_webbrowser(question)
    elif al_num == 2:
        open_webbrowser_count(question, choices, q)
    elif al_num == 3:
        count_base(question, choices, q)
    elif al_num == 1:
        cloud_count(question, q)

if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


