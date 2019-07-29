#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : demo.py 
# @Software: PyCharm
# @Time : 2019/7/26 16:50

import requests
import json
import utils.file.img as img
import utils.encodes as encodes
import utils.request as request


if __name__ == '__main__':
    url_request = 'https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens'
    token_data = {
        'auth': {
            'identity': {
                'methods': ['password'],
                'password': {
                    'user': {
                        'name': 'Zackeus',
                        'password': 'syr391592723*',
                        'domain': {'name': 'Zackeus'}
                    }
                }
            },
            'scope': {
                'project': {'name': 'cn-north-1'}
            }
        }
    }

    res = requests.post(url=url_request, data=json.dumps(obj=token_data), headers=request.ContentType.JSON_UTF8.value)
    res.encoding = encodes.Unicode.UTF_8.value

    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    url = 'https://ocr.cn-north-1.myhuaweicloud.com/v1.0/ocr/mvs-invoice'
    x_token = res.headers['X-Subject-Token']
    print(x_token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Auth-Token': x_token
    }

    base_str = img.ImgUtil.img_compress(
        path='D:/AIData/OCR/11.JPG',
        threshold=0.5
    )
    params = {
        'image': base_str
    }

    res = requests.post(url=url, data=json.dumps(obj=params), headers=headers)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
