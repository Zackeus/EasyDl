#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : demo.py 
# @Software: PyCharm
# @Time : 2019/7/22 11:45


import urllib.request
import urllib.parse
import json
import time
import base64
import requests

from utils import encodes


def posturl(url,data={}):
  try:
    params=json.dumps(dict).encode(encoding='UTF8')
    req = urllib.request.Request(url, params, headers)
    r = urllib.request.urlopen(req)
    html =r.read()
    r.close();
    return html.decode("utf8")
  except urllib.error.HTTPError as e:
      print(e.code)
      print(e.read().decode("utf8"))
  time.sleep(1)


if __name__ == '__main__':
    headers = {
        'Authorization': 'APPCODE 4609757e6ff24139844d629bc2d73823',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    with open('D:/AIData/OCR/4.JPG', 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        encodestr = str(base64.b64encode(data), 'utf-8')

    url_request = "https://ocrapi-car-invoice.taobao.com/ocrservice/carInvoice"
    dict = {'img': encodestr}

    res = requests.post(url=url_request, data=json.dumps(obj=dict), headers=headers)
    res.encoding = encodes.Unicode.UTF_8.value

    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
