# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 19:34
# @desc    :

from PIL import Image
import pytesseract
from PIL import ImageFilter
from aip import AipOcr
import io
import base64
from colorama import init,Fore

# 根据自己的手机或者模拟器修改这个题目与选项区域即可
# 分别截题目和选项
question_region = [50, 350, 1000, 560]
choices_region = [75, 535, 1000, 1200]

# 题目和选项一起截
combine_region = [50, 350, 1000, 1200]

# 二值化算法
def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


# 去除干扰线算法
def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img


def ocr_img(image):

    global question_region, choices_region, combine_region

    question_im = image.crop((question_region[0], question_region[1], question_region[2], question_region[3])) # 坚果 pro1
    choices_im = image.crop((choices_region[0], choices_region[1], choices_region[2], choices_region[3]))


    # 边缘增强滤波,不一定适用
    #question_im = question_im.filter(ImageFilter.EDGE_ENHANCE)
    #choices_im = choices_im.filter(ImageFilter.EDGE_ENHANCE)

    # 转化为灰度图
    question_im = question_im.convert('L')
    choices_im = choices_im.convert('L')

    # 把图片变成二值图像
    question_im = binarizing(question_im, 190)
    choices_im = binarizing(choices_im, 190)

    #question_im = question_im.convert('1')
    #choices_im = choices_im.convert('1')
    #question_im.show()
    #choices_im.show()
    # img=depoint(choices_im)
    # img.show()

    # win环境
    # tesseract 路径
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    # 语言包目录和参数
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6'

    # mac 环境 记得自己安装训练文件
    # tesseract 路径
    #pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'
    # 语言包目录和参数
    #tessdata_dir_config = '--tessdata-dir "/usr/local/Cellar/tesseract/3.05.01/share/tessdata/" --psm 6'
    
    # lang 指定中文简体
    question = pytesseract.image_to_string(question_im, lang='chi_sim', config=tessdata_dir_config)
    question = question.replace("\n", "")[2:]
    # 处理将"一"识别为"_"的问题
    question = question.replace("_", "一")


    choice = pytesseract.image_to_string(choices_im, lang='chi_sim', config=tessdata_dir_config)
    # 处理将"一"识别为"_"的问题
    choices = choice.strip().replace("_", "一").split("\n")
    choices = [ x for x in choices if x != '' ]

    # 兼容截图设置不对，意外出现问题为两行或三行
    # if (choices[0].endswith('?')):
    #     question += choices[0]
    #     choices.pop(0)
    # if (choices[1].endswith('?')):
    #     question += choices[0]
    #     question += choices[1]
    #     choices.pop(0)
    #     choices.pop(1)

    return question, choices

def ocr_img_tess(image):
    """只运行一次 Tesseract"""

    global combine_region

    # 切割题目+选项区域，左上角坐标和右下角坐标,自行测试分辨率
    region_im = image.crop((combine_region[0], combine_region[1], combine_region[2], combine_region[3]))

    # 转化为灰度图
    region_im = region_im.convert('L')

    # 把图片变成二值图像
    region_im = binarizing(region_im, 190)

    #region_im.show()

    # win环境
    # tesseract 路径
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    # 语言包目录和参数
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6'

    # mac 环境 记得自己安装训练文件
    # tesseract 路径
    # pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'
    # 语言包目录和参数
    # tessdata_dir_config = '--tessdata-dir "/usr/local/Cellar/tesseract/3.05.01/share/tessdata/" --psm 6'

    # lang 指定中文简体
    region_text = pytesseract.image_to_string(region_im, lang='chi_sim', config=tessdata_dir_config)
    region_text = region_text.replace("_", "一").split("\n")
    texts = [x for x in region_text if x != '']
    #print(texts)
    if len(texts) > 2:
        question = texts[0]
        choices = texts[1:]
    else:
        print(Fore.RED + '截图区域设置错误，请重新设置' + Fore.RESET)
        exit(0)

    # 意外出现问题为两行或三行
    if choices[0].endswith('?'):
        question += choices[0]
        choices.pop(0)
    elif choices[1].endswith('?'):
        question += choices[0]
        question += choices[1]
        choices.pop(0)
        choices.pop(1)

    return question, choices

def ocr_img_baidu(image):
    # 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
    """ 你的 APPID AK SK """
    APP_ID = '10657697'
    API_KEY = '5dQBPnsySGnrQGD9UZNaOYCX'
    SECRET_KEY = '26ISs5EC4xdGSDoYYKYKrEIAFDqZlGXG'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    global combine_region
    # 切割题目+选项区域，左上角坐标和右下角坐标,自行测试分辨率
    region_im = image.crop((combine_region[0], combine_region[1], combine_region[2], combine_region[3]))

    img_byte_arr = io.BytesIO()
    region_im.save(img_byte_arr, format='PNG')
    image_data = img_byte_arr.getvalue()
    #base64_data = base64.b64encode(image_data)
    response = client.basicGeneral(image_data)
    words_result = response['words_result']

    texts = [x['words'] for x in words_result]
    #print(texts)
    if len(texts) > 2:
        question = texts[0]
        choices = texts[1:]
        choices = [x.replace(' ', '') for x in choices]
    else:
        print(Fore.RED + '截图区域设置错误，请重新设置' + Fore.RESET)
        exit(0)

    # 意外出现问题为两行或三行
    if choices[0].endswith('?'):
        question += choices[0]
        choices.pop(0)
    elif choices[1].endswith('?'):
        question += choices[0]
        question += choices[1]
        choices.pop(0)
        choices.pop(1)


    return question, choices


if __name__ == '__main__':
    image = Image.open("../screenshot.png")
    question, choices = ocr_img_tess(image)
    print("Tess 识别结果:")
    print(question)
    print(choices)
    print()

    question, choices = ocr_img_baidu(image)
    print("baidu 识别结果:")
    print(question)
    print(choices)