#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : nlp.py 
# @Software: PyCharm
# @Time : 2019/5/23 15:08


import requests
import json
from marshmallow import Schema, fields, post_load

from utils.errors import MyError
from utils.encodes import Unicode
from utils.request import codes, ContentType
from utils.object_util import is_not_empty, BaseObject
from utils.baidu_cloud.baidu import BaiduCloud
from utils.decorators import auto_wired


class NLP(BaseObject):

    def __init__(self, api_key=None, secret_key=None, baidu_cloud=None):
        """
        自然语言处理
        :param api_key:
        :param secret_key:
        :param baidu_cloud:
        """

        self.token = None
        if is_not_empty(api_key) and is_not_empty(secret_key):
            baidu_cloud = BaiduCloud(api_key, secret_key)
            baidu_cloud.init_token()
        elif is_not_empty(baidu_cloud) and is_not_empty(baidu_cloud.token):
            pass
        else:
            raise MyError('缺失鉴权 Token 参数.')
        self.token = baidu_cloud.token

    def lexer(self, url, text):
        """
        词法分析
        :param url:
        :param text:
        :return:
        """
        url = url.format(access_token=self.token)
        res = requests.post(url=url, data=json.dumps(obj={'text': text}), headers=ContentType.JSON_UTF8.value)
        res.encoding = Unicode.UTF_8.value
        return res


if __name__ == '__main__':
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer_custom?charset=UTF-8&access_token={access_token}'
    text = '百度是一家高科技公司'
    nlp = NLP('6wheIPDCYOQy0nAjjkWPplT9', 'Q1SxbGtr9OLPzIpbQA3YD9CWda1H7zHk')
    res = nlp.lexer(url, text)
    print(res)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
