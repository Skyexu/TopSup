
# 答题辅助
这两天冲顶大会直播答题 APP 突然火了起来，萌生了使用截图，文字识别，搜索来做个小辅助的想法。使用文字识别搜索，只能增加准确率，保证不了全对。



**非常感谢关注，欢迎大家PR新的想法和优化。**

![](/resources/screenshot.png)

灵感来自：
> [微信跳一跳辅助 ](https://github.com/wangshub/wechat_jump_game)
>
> [程序员如何玩转《冲顶大会》？](https://livc.io/blog/204)

## FORK 更新

- 自动识别问题为多行情况
- 无需手动操作手机，自动选择正确答案
- 自动识别正确答案
- 同步答案到网络上，方便大家参考
- 发布了 release 


## 更新日志
- 2018.01.12
  - 修复 windows 命令行颜色乱码，处理一些识别错误
- 2018.01.11
  - 修复搜索可能的乱码等一些问题，多线程加快执行
- 2018.01.10
  - 增加循环，无需重复加载，优化逻辑和显示 来自 [issue #7](https://github.com/Skyexu/TopSup/issues/7)。增加部分手机截图设置
  - 增加了截图传输效率，修改了识别参数，对图像进行灰度转化，去干扰，增加了识别准确率。结果判断使用了三种方式，对不同问题可以参考不同结果。


## 版本说明
- 谷歌 Tesseract
  - [简单访问浏览器版本](/simpleVersion)
  - 最新版本：本目录
- [百度 OCR 版本](https://github.com/Skyexu/TopSup/tree/master/baiduApiVersion)：只实现了简单浏览器搜索，参考本目录代码可改



## 具体做法

1. ADB 获取手机截屏
```
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .
```
2. OCR 识别题目与选项文字   

  ![](/resources/cut.png)

  ​
  两个方法：

  - 谷歌 [Tesseract](https://github.com/madmaze/pytesseract) ，安装软件即可，接下来主要使用这个方法
  - [百度 OCR](https://cloud.baidu.com/product/ocr) ，[需要]()注册百度 API，每天调用次数有限

3. 搜索判断

## 结果判断方式

1. 直接打开浏览器搜索问题
  ![](./resources/result.png)
2. 题目+每个选项都通过搜索引擎搜索，从网页代码中提取搜索结果计数
3. 只用题目进行搜索，统计结果页面代码中包含选项的词频

以下为两个示例结果

![](./resources/result2.png)

![](./resources/result3.png)

参考了 [I Hacked HQ Trivia But Here’s How They Can Stop Me](https://hackernoon.com/i-hacked-hq-trivia-but-heres-how-they-can-stop-me-68750ed16365)

## 使用步骤 (谷歌 [Tesseract](https://github.com/madmaze/pytesseract)) 
### Android

#### 1. 安装 ADB

**windows**

下载地址：https://adb.clockworkmod.com/

**Mac**

使用 brew 进行安装 `brew cask install android-platform-tools`



安装完后插入安卓设备且安卓已打开 USB 调试模式，终端输入 `adb devices` ，显示设备号则表示成功。我手上的机子是坚果 pro1，第一次不成功,查看设备管理器有叹号，使用 [handshaker](https://www.smartisan.com/apps/handshaker) 加载驱动后成功，也可以使用豌豆荚之类的试试。

```
List of devices attached
6934dc33    device
```

若不成功，可以参考[Android 和 iOS 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)进行修改

#### 2. 安装 python 3
#### 3. 安装所需 python 包

命令行：
`pip install -r requirements.txt`

或者
```
pip install pytesseract
pip install pillow  
pip install requests
pip install colorama

```
#### 4. 安装 谷歌 Tesseract

Windows下链接：
*推荐使用安装版，在安装时选择增加中文简体语言包*
- 安装版：
  https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.01.exe
- 免安装版：
  https://github.com/parrot-office/tesseract/releases/download/3.5.1/tesseract-Win64.zip
  *免安装版需要下载[中文语言包](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files)，放置到Tesseract的`tessdata`目录下*

其他系统：
https://github.com/tesseract-ocr/tesseract/wiki

#### 5. 修改  `common/ocr.py` 代码相应目录信息
```
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
```

#### 6. 运行脚本
`python GetQuestionTessAndroid.py`
会自动识别文字并打开浏览器

**注： 可以用 `GetImgTool.py` 调整题目截取位置**
可以到[这里](/config/devicesCutConfig.txt)查看部分手机截图设置
若屏幕分辨率不同，请在 `ocr.py` 中自行修改代码即可
```
# 切割题目和选项位置，左上角坐标和右下角坐标,自行测试分辨率
question_im = image.crop((50, 350, 1000, 560)) # 坚果 pro1
choices_im = image.crop((75, 535, 990, 1150))
# question = img.crop((75, 315, 1167, 789)) # iPhone 7P
```

### IOS

**部分朋友成功**

- 需要安装 WDA 进行截图，参考
  -  [iOS 真机如何安装 WebDriverAgent](https://testerhome.com/topics/7220) 
  -  [Android 和 iOS 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)
- 安装 [python-wda](https://github.com/openatx/facebook-wda)
- 其他步骤相同。
- `python GetQuestionTessIos.py`

## 使用步骤 (百度 OCR)

请移步，[链接](/baiduApiVersion)

## 其它
- Tesseract 参数，若识别有问题可以更改参数解决
  https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc
- 三种方法可以选择，可以加#注释掉只保留一个方法
- windows 命令行有很多乱码问题，建议使用 cmder 作为命令工具，可以支持 linux 命令


## 总结

有了 ADB 截图，怕是各种小辅助都可以玩了。python 写小脚本真的很方便。

## Next

- 文字识别后 nlp 处理一下关系，然后搜索不同选择结果
