# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/10 19:22
# @desc    : 仅限冲顶大会, 调用 api 无需截图，运行更快
import requests
import json
from common import  methods



#dic = {"code":0,"msg":"成功","data":{"event":{"answerTime":10,"correctOption":1,"desc":"12.“清乾隆各种釉彩大瓶”装饰的釉、彩共达多少层？","displayOrder":11,"liveId":91,"options":"[\"16\",\"17\",\"18\"]","questionId":1023,"showTime":1515582915149,"stats":[2695,4932,4710],"status":2,"type":"showAnswer"},"type":"showAnswer"}}



while True:
    resptext = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current', timeout=5).text
    resptext_dict = json.loads(resptext)
    #print(resptext_dict)
    if resptext_dict['msg'] == 'no data':
        print('题目还没出来，请稍后再试')
    else:
        question = dic['data']['event']['desc'][2:]
        ch = dic['data']['event']['options']
        ch = ch[1:len(ch) - 1].replace('"', '')
        choices = ch.split(',')

        # 用不同方法输出结果，取消某个方法在前面加上#

        # 打开浏览器方法搜索问题
        methods.run_algorithm(0, question, choices)
        # 将问题与选项一起搜索方法，并获取搜索到的结果数目
        methods.run_algorithm(1, question, choices)
        # 用选项在问题页面中计数出现词频方法
        methods.run_algorithm(2, question, choices)

    go = input('输入回车继续运行,输入 n 回车结束运行: ')
    if go == 'n':
        break

    print('------------------------')


