# -*- coding: utf-8 -*-
"""
手机屏幕截图的代码 ，用管道或取图片数据比直接传输图片快，来自 https://github.com/wangshub/wechat_jump_game
"""
import subprocess
import os
import sys
from PIL import Image
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('./config/configure.conf', encoding='utf-8')


# SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
SCREENSHOT_WAY = 3


def pull_screenshot():
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序
    """
    global SCREENSHOT_WAY

    # 兼容多个adb设备的情况
    device_cmd = ''
    try:
        devices = os.popen('adb devices').readlines()[1:-1]
        devices_count = len(devices)
        if devices_count > 1:
            adb_device = config.get('device', 'adb_device')
            device_cmd = ' -s ' + adb_device
        elif devices_count == 0:
            print('当前暂无已连接的adb设备')
            exit(0)
    except Exception:
        pass

    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            'adb' + device_cmd + ' shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
            # binary_screenshot = binary_screenshot.split(b' ')
            # binary_screenshot = binary_screenshot[len(binary_screenshot) - 1]
            # print(binary_screenshot)
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        f = open('screenshot.png', 'wb')
        f.write(binary_screenshot)
        f.close()
    elif SCREENSHOT_WAY == 0:
        os.system('adb' + device_cmd +
                  ' shell screencap -p /sdcard/screenshot.png')
        os.system('adb' + device_cmd + ' pull /sdcard/screenshot.png .')


def check_screenshot():
    """
    检查获取截图的方式
    """
    global SCREENSHOT_WAY
    if os.path.isfile('screenshot.png'):
        try:
            os.remove('screenshot.png')
        except Exception:
            pass
    if SCREENSHOT_WAY < 0:
        print('暂不支持当前设备')
        sys.exit()
    pull_screenshot()
    try:
        Image.open('./screenshot.png').load()
        print('采用方式 {} 获取截图'.format(SCREENSHOT_WAY))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot()

if __name__ == '__main__':
    check_screenshot()
    img = Image.open("./screenshot.png")