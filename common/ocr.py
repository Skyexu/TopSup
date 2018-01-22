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

global os
os = 'cd'

def get_question(image, question_end):
    global os

    w,h = image.size
    #支持平板 
    if (w>h):
        image = image.transpose(Image.ROTATE_270) 
        temp = w
        w = h
        h = temp

    im_pixel = image.load()

    if (os=='zs'):
        #芝士超人
        answer_height = 100
    elif (os=='hj' or os =='cd'):
        #花椒直播
        # 冲顶大会
        answer_height = 150

    # 自动识别答案位置
    piece_y_max = question_end
    scan_x_border = 75
    scan_start_y =  piece_y_max
    for i in range(scan_start_y, h):
        if (piece_y_max != question_end):
            break
        for j in range(scan_x_border, scan_x_border+100):
            pixel = im_pixel[j, i]
            if (abs(pixel[1]-pixel[0])>50 or abs(pixel[1]-pixel[2])>50):
                piece_y_max = max(i, piece_y_max)
                break
    print(question_end)
    print(piece_y_max)
    print(answer_height)
    return round((piece_y_max-question_end)/answer_height)


def ocr_img(image):
    global os

    w,h = image.size
    #读取图像 

    #支持平板 
    if (w>h):
        image = image.transpose(Image.ROTATE_270) 
        temp = w
        w = h
        h = temp

    im_pixel = image.load()

    print(os)
    if (os=='zs'):
        #芝士超人
        # 自动识别问题开始
        scan_x_border = int(w / 4)
        scan_start_y = 200 
        question_start = 200
        for i in range(scan_start_y, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if (pixel[1]==255 and pixel[1]==255 and pixel[2]==255):
                    white_sum = white_sum + 1
            if (white_sum!=100):
                question_start = max(i, question_start)
                break;


        # 自动识别问题结束
        scan_x_border = int(w / 4)
        scan_start_y = question_start 
        question_end = question_start
        for i in range(scan_start_y, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if (abs(200-pixel[0])<50 and (200-pixel[1])<50 and (200-pixel[2])<50):
                    white_sum = white_sum + 1

            if (white_sum==100):
                question_end = max(i, question_end)
                break;

        if(question_start == question_end):
            return '', [], 0

        print(question_start)
        print(question_end)
        question_im = image.crop((50, question_start, 1000, question_end)) 

        # 自动识别题板高度
        piece_y_max = question_end
        scan_x_border = int(w / 2)
        scan_start_y =  piece_y_max
        for i in range(scan_start_y, h):
            if (piece_y_max != question_end):
                break
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if (abs(pixel[1]-pixel[0])>3 or abs(pixel[1]-pixel[2])>3):
                    piece_y_max = max(i, piece_y_max)
                    break

        choices_im = image.crop((75, question_end, 1000, piece_y_max))

        answer_height = 100

    if (os=='hj'):
        #花椒直播
        # 自动识别问题开始

        scan_x_border = int(w / 2)
        scan_start_y = 300 
        question_start = 300
        for i in range(scan_start_y, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if ((255-pixel[0])<10 and (255-pixel[1])<10 and (255-pixel[2])<10):
                    white_sum = white_sum + 1
            if (white_sum!=100):
                question_start = max(i, question_start)
                break;


        # 自动识别问题结束
        scan_x_border = int(w / 2)
        scan_start_y = question_start 
        question_end = question_start
        for i in range(scan_start_y, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if (abs(220-pixel[0])<20 and abs(220-pixel[1])<20 and abs(220-pixel[2])<20 ):
                    white_sum = white_sum + 1
            if (white_sum==100):
                question_end = max(i, question_end)
                break;

        if(question_start == question_end):
            return '', [], 0

        question_im = image.crop((50, question_start, 1000, question_end)) 

        # 自动识别题板高度
        piece_y_max = question_end
        scan_x_border = int(w / 2)
        for i in range(question_end, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if (pixel[0]<100 and pixel[1]<100 and pixel[2]<100):
                    white_sum = white_sum + 1
            if (white_sum>90):
                piece_y_max = max(i, piece_y_max)
                break;

        choices_im = image.crop((75, question_end, 1000, piece_y_max))

        answer_height = 150

    if (os=='cd'):
        # 冲顶大会
        # 自动识别问题开始
        scan_x_border = int(w / 2)
        scan_start_y = 100 
        question_start = 100
        for i in range(scan_start_y, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if ((255-pixel[0])<10 and (255-pixel[1])<10 and (255-pixel[2])<10):
                    white_sum = white_sum + 1
            if (white_sum!=100):
                question_start = max(i, question_start)
                break;


        # 自动识别问题结束
        scan_x_border = int(w / 2)
        scan_start_y = question_start 
        question_end = question_start
        for i in range(scan_start_y, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if (abs(200-pixel[0])<10 and abs(200-pixel[1])<10 and abs(200-pixel[2])<10):
                    white_sum = white_sum + 1
            if (white_sum==100):
                question_end = max(i, question_end)
                break;

        question_im = image.crop((50, question_start, 1000, question_end)) 

        # 自动识别题板高度
        piece_y_max = question_end
        scan_x_border = int(w / 2)
        for i in range(question_end, h):
            white_sum=0
            for j in range(scan_x_border-50, scan_x_border+50):
                pixel = im_pixel[j, i]
                if (pixel[0]<100 and pixel[1]<100 and pixel[2]<100):
                    white_sum = white_sum + 1
            if (white_sum>10):
                piece_y_max = max(i, piece_y_max)
                break;

        choices_im = image.crop((75, question_end, 1000, piece_y_max))

        answer_height = 150

    if(question_start == question_end or question_end == piece_y_max):
        return '', [], 0

    print(question_end)
    print(piece_y_max)
    # question = image.crop((75, 315, 1167, 789)) # iPhone 7P
    question_im.save('question.jpg');
    choices_im.save('choices.jpg');
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

    print(choices)
    choices = [ x for x in choices if x != '' ]
    print(choices)
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

    print(choices)
    return question, choices, question_end


if __name__ == '__main__':
    image = Image.open("./screenshot.png")
    question,choices = ocr_img(image)

    print("识别结果:")
    print(question)
    print(choices)