# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser
import urllib.parse
from pyquery import PyQuery as pq

# # 颜色兼容Win 10
from colorama import init,Fore,Back
init()

def open_webbrowser(question):
    webbrowser.open('https://baidu.com/s?wd=' + urllib.parse.quote(question))

def open_webbrowser_count(question,choices):
    print('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
    print('Question: ' + question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')

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
    output(choices, counts)

def count_base(question,choices):
    print('\n-- 方法3： 题目搜索结果包含选项词频计数法 --\n')
    # 请求
    question = '寒食节是为了纪念谁'
    choices = ['屈原','介之推','鲁迅']
    req = requests.get(url='http://www.baidu.com/s', params={'wd':question})
    content = req.text
    doc = pq(content)
    content = doc.find('#content_left').html()
    baike_content = doc.find('.op_exactqa_main').html()
    counts = []
    baike_recommend = ''
    print('Question: '+question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')
    for i in range(len(choices)):
        counts.append(content.count(choices[i]))
        if baike_content and baike_content.count(choices[i]):
            baike_recommend = choices[i]
        #print(choices[i] + " : " + str(counts[i]))
    output(choices, counts)

    if baike_recommend:
        print()
        print(Fore.YELLOW + '{0}：{1}'.format('百科推荐', baike_recommend) + Fore.RESET)
        print()


def output(choices, counts):
    counts = list(map(int, counts))
    #print(choices, counts)

    # 计数最高
    index_max = counts.index(max(counts))

    # 计数最少
    index_min = counts.index(min(counts))

    if index_max == index_min:
        print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        return
    print(Back.WHITE)
    for i in range(len(choices)):
        print()
        if i == index_max:
            # 绿色为计数最高的答案
            print(Fore.GREEN + "选项 {0} ---- {1} : {2} ".format(str(i + 1), choices[i], counts[i]) + Fore.RESET)
        elif i == index_min:
            # 红色为计数最低的答案
            print(Fore.MAGENTA + "选项 {0} ---- {1} : {2}".format(str(i + 1), choices[i], counts[i]) + Fore.RESET)
        else:
            print(Fore.BLACK + "选项 {0} ---- {1} : {2}".format(str(i + 1), choices[i], counts[i]) + Fore.RESET)
    
    print(Back.RESET)

def run_algorithm(al_num, question, choices):
    if al_num == 0:
        # open_webbrowser(question)
	    pass
    elif al_num == 1:
        open_webbrowser_count(question, choices)
    elif al_num == 2:
        count_base(question, choices)

if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


