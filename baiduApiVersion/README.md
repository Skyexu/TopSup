# 百度 ocr api 版本
只实现了简单的浏览器搜索问题，更多方式其实拷贝一下代码就好啦。

1. 安装 ADB
2. 安装 python 3
3. 安装所需 python 包
```
urllib
requests
base64
```
4. 在[百度平台](https://cloud.baidu.com/product/ocr)上创建应用申请 API Key 和 Secret Key
5. 在 `GetTitleBaiduAndroid.py` 中加入相应 key
```
# 百度OCR API
api_key = ''
api_secret = ''
```
6. 运行脚本 
安卓： `python GetTitleBaiduAndroid.py`
IOS： `python GetTitleBaiduIos.py`