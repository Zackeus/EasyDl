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


def to_ocr(x_token, img_path):
    url = 'https://ocr.cn-north-1.myhuaweicloud.com/v1.0/ocr/mvs-invoice'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Auth-Token': x_token
    }

    base_str = img.ImgUtil.img_compress(
        path=img_path,
        threshold=10
    )
    params = {
        'image': base_str
    }

    res = requests.post(url=url, data=json.dumps(obj=params), headers=headers)
    print(res.status_code)
    # print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    return res.json()


if __name__ == '__main__':
    import os
    from utils.file import FileUtil

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
    x_token = res.headers['X-Subject-Token']

    for file_path in FileUtil.get_files_by_suffix2('D:/AIData/zhouUcl', ['jpg']):
        path, name, ext = FileUtil.get_path_name_ext(file_path)
        total = float(name.split('-')[0])
        dirs = 'D:/AIData/OCR/{0}'.format(name)
        FileUtil.copy_file(file_path, dirs)

        ocr_json = to_ocr(x_token, file_path)
        ocr_total = ocr_json.get('result').get('total')

        with open(os.path.join(dirs, 'ocr.txt'), 'w') as f:
            f.write(json.dumps(ocr_json, indent=4, ensure_ascii=False))

        os.rename(dirs, '{0}-{1}'.format(dirs, ocr_total))
        print(name, ocr_total)
        FileUtil.del_file(file_path)







