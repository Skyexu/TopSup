# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser

def open_webbrowser(question):
    webbrowser.open('https://baidu.com/s?wd=' + question)

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
    req = requests.get(url='http://www.baidu.com/s', params={'wd':question})
    content = req.text
    #print(content)
    counts = []
    print('Question: '+question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')
    for i in range(len(choices)):
        counts.append(content.count(choices[i]))
        #print(choices[i] + " : " + str(counts[i]))
    output(choices, counts)

def output(choices, counts):
    counts = list(map(int, counts))
    #print(choices, counts)

    # 最可能的答案
    index_max = counts.index(max(counts))

    # 最不可能的答案
    index_min = counts.index(min(counts))

    if index_max == index_min:
        print("\033[1;31m此方法失效！\033[0m")
        return

    for i in range(len(choices)):
        if i == index_max:
            # 绿色为计数最高的答案
            print("\033[1;32m{0:^10} {1:^10}\033[0m".format(choices[i], counts[i]))
        elif i == index_min:
            # 红色为计数最低的答案
            print("\033[0;31m{0:^10}{1:^10}\033[0m".format(choices[i], counts[i]))
        else:
            print("{0:^10} {1:^10}".format(choices[i], counts[i]))


def run_algorithm(al_num, question, choices):
    if al_num == 0:
        open_webbrowser(question)
    elif al_num == 1:
        open_webbrowser_count(question, choices)
    elif al_num == 2:
        count_base(question, choices)

if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


