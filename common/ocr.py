# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 19:34
# @desc    :

from PIL import Image
import pytesseract
from PIL import ImageFilter

# 二值化算法
def binarizing(img,threshold):
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

    # 切割题目和选项位置，左上角坐标和右下角坐标,自行测试分辨率
    w,h = image.size
    question_im = image.crop((50, 350, 1000, 560)) # 坚果 pro1

    # 自动识别题板高度
    # white_sum = 0
    piece_y_max = 1150
    im_pixel = image.load()
    scan_x_border = int(w / 2)
    scan_start_y = int(h / 2) 
    for i in range(scan_start_y, h):
        white_sum=0
        for j in range(scan_x_border-50, scan_x_border+50):
            pixel = im_pixel[j, i]
            if (abs(pixel[1]-pixel[0])<5 and abs(pixel[1]-pixel[2])<5):
                white_sum = white_sum + 1
        if (white_sum<20):
            piece_y_max = max(i, piece_y_max)
            break;

    choices_im = image.crop((75, 535, 990, piece_y_max))
    # question = image.crop((75, 315, 1167, 789)) # iPhone 7P

    # 边缘增强滤波,不一定适用
    #question_im = question_im.filter(ImageFilter.EDGE_ENHANCE)
    #choices_im = choices_im.filter(ImageFilter.EDGE_ENHANCE)

    # 转化为灰度图
    question_im = question_im.convert('L')
    choices_im = choices_im.convert('L')
    # 把图片变成二值图像
    question_im = binarizing(question_im, 190)
    choices_im = binarizing(choices_im, 190)
    #img=depoint(choices_im)
    #img.show()

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

    # 兼容问题为多行
    question_length = 0
    for i in range(len(choices)):
        if (choices[i].endswith('?')):
            j=0
            while (j<i):
                question += choices[j]
                j=j+1
            j=i
            while (j>-1):
                choices.pop(j)
                j=j-1
            question_length = i;
            break
    i=0
    while (len(choices)>3):
        choices.pop()        

    return question, choices


if __name__ == '__main__':
    image = Image.open("./screenshot.png")
    question,choices = ocr_img(image)

    print("识别结果:")
    print(question)
    print(choices)