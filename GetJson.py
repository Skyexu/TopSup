# coding: utf-8
# quote from kmaiya/HQAutomator
# cddh原版搬运，增加了在线模拟接口。大神可以补充进一步的问题加选项的搜索算法

import time
import json
import requests
import webbrowser

questions = []


def get_answer():
    #正式环境
    resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current',timeout=4).text

    #在线模拟调试json接口
    #resp = requests.get('http://www.mocky.io/v2/5a56d6f52e0000cc0711feca', timeout=4).text
    resp_dict = json.loads(resp)
    if resp_dict['msg'] == 'no data':
        return 'Waiting for question...'
    else:
        resp_dict = eval(str(resp))
        question = resp_dict['data']['event']['desc']
        question = question[question.find('.') + 1:question.find('?')]
        options = resp_dict['data']['event']['options']
        if question not in questions:
            questions.append(question)
            webbrowser.open("https://www.baidu.com/s?ie=UTF-8&wd=" + question)
        else:
            return 'Waiting for new question...'

        print(options)
def main():
    while True:
        print(time.strftime('%H:%M:%S',time.localtime(time.time())))
        print(get_answer())
        time.sleep(1)


if __name__ == '__main__':
    main()
