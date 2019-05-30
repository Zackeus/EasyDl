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

from utils import encodes
from utils.errors import MyError
from utils.request import codes, ContentType
from utils.object_util import is_not_empty, is_empty, BaseObject
from utils.baidu_cloud.baidu import BaiduCloud
from utils.decorators import auto_wired
from utils.assert_util import Assert


class NLP(BaseObject):

    @auto_wired('utils.baidu_cloud.nlp.NLP')
    def __init__(self, api_key=None, secret_key=None, baidu_cloud=None, **kwargs):
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

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def lexer(self, text, ne_list=[], url=None):
        """
        词法分析
        :param url:
        :param text:
        :param ne_list: 过滤命名实体类型
        :return:
        """
        url = url if url else getattr(self, 'lexer_url', None)
        url = url.format(access_token=self.token)
        res = requests.post(url=url, data=json.dumps(obj={'text': text}), headers=ContentType.JSON_UTF8.value)
        res.encoding = encodes.Unicode.UTF_8.value

        if res is None or res.status_code != codes.ok:
            raise MyError(code=codes.failed, msg='百度词法分析请求失败.')

        lexer_res, errors = LexerRes.LexerResSchema().load(res.json())  # type: LexerRes
        Assert.is_true(is_empty(errors), errors)

        if is_not_empty(ne_list):
            for lexer_item in lexer_res.items[:]:
                if lexer_item.ne not in ne_list:
                    # 根据实体列表过滤
                    lexer_res.items.remove(lexer_item)
        return lexer_res


class LexerItem(BaseObject):

    def __init__(self, item, ne, pos, byte_offset, byte_length,
                 uri, basic_words, formal=''):
        """
        词性分析字符串
        :param str item: 词汇的字符串
        :param str ne: 命名实体类型，命名实体识别算法使用。词性标注算法中，此项为空串
        :param str pos: 词性，词性标注算法使用。命名实体识别算法中，此项为空串
        :param int byte_offset: 在text中的字节级offset
        :param int byte_length: 字节级length
        :param str uri: 链指到知识库的URI，只对命名实体有效。对于非命名实体和链接不到知识库的命名实体，此项为空串
        :param list basic_words: 基本词成分
        :param str formal: 词汇的标准化表达，主要针对时间、数字单位，没有归一化表达的，此项为空串
        """
        self.item = item
        self.ne = ne
        self.pos = pos
        self.byte_offset = byte_offset
        self.byte_length = byte_length
        self.uri = uri
        self.basic_words = basic_words
        self.formal = formal

    class LexerItemSchema(Schema):
        item = fields.Str(required=True)
        ne = fields.Str(required=True)
        pos = fields.Str(required=True)
        byte_offset = fields.Integer(required=True)
        byte_length = fields.Integer(required=True)
        uri = fields.Str(required=True)
        basic_words = fields.List(fields.Str(), required=True)
        formal = fields.Str()

        @post_load
        def make_object(self, data):
            return LexerItem(**data)


class LexerRes(BaseObject):

    def __init__(self, log_id, text, items):
        """
        词性分析返回结果
        :param long log_id: 唯一的log id，用于问题定位
        :param str text: 原始单条请求文本
        :param list items: 词汇数组，每个元素对应结果中的一个词
        """
        self.log_id = log_id
        self.text = text
        self.items = items

    class LexerResSchema(Schema):
        log_id = fields.Integer(required=True)
        text = fields.Str(required=True)
        items = fields.Nested(LexerItem.LexerItemSchema, required=True, many=True)

        @post_load
        def make_object(self, data):
            return LexerRes(**data)


if __name__ == '__main__':
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer_custom?charset=UTF-8&access_token={access_token}'
    ne_list = ['PER', 'LOC', 'ORG', 'TIME', 'TBW', 'TOA', ]
    # text = '我这边裕隆汽车金融的，跟您核对一下您的汽车贷款的信息方方便！'
    text = '现在居住是在康乐富城康乐县富城滨河镇路'
    # text = '谢尔盖·科罗廖夫（1907年1月12日－1966年1月14日），原苏联宇航事业的伟大设计师与组织者'
    nlp = NLP('6wheIPDCYOQy0nAjjkWPplT9', 'Q1SxbGtr9OLPzIpbQA3YD9CWda1H7zHk')
    lexer_res = nlp.lexer(url=url, text=text, ne_list=ne_list)

    for lexer_item in lexer_res.items:
        print(lexer_item)


