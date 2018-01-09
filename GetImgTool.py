# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 00:40
# @desc    : adb 获取截屏，截取图片


from PIL import Image
import os
import matplotlib.pyplot as plt

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')

pull_screenshot()
img = Image.open("./screenshot.png")

# 用 matplot 查看测试分辨率，切割问题和选项区域
#region = img.crop((75, 315, 1167, 789)) # iPhone 7P

question  = img.crop((50, 350, 1000, 560)) # 坚果 pro1
choices = img.crop((75, 535, 990, 1130))

plt.subplot(221)
im = plt.imshow(img, animated=True)
plt.subplot(222)
im2 = plt.imshow(question, animated=True)
plt.subplot(212)
im3 = plt.imshow(choices, animated=True)
plt.show()