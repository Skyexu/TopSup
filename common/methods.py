# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser

def open_webbrowser(question):
    webbrowser.open('https://baidu.com/s?wd=' + question)

def count_base(question,choices):
    # 请求
    req = requests.get(url='http://www.baidu.com/s', params={'wd':question})
    content = req.text

    counts = []
    print('Question: '+question)
    for i in range(len(choices)):
        counts.append(content.count(choices[i]))
        print(choices[i] + " : " + str(counts[i]))
    print('Recommend Choose : ' + choices[counts.index(max(counts))])



def run_algorithm(al_num,question,choices):
    if al_num == 0:
        open_webbrowser(question)
    elif al_num == 1:
        count_base(question, choices)

if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['甲醛', '苯', '甲醇']
    count_base(question, choices)

