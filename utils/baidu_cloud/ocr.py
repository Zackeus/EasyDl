#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : ocr.py 
# @Software: PyCharm
# @Time : 2019/9/10 15:27


import json
import requests
from marshmallow import fields, Schema, pre_load, post_load

from extensions import db
from utils.baidu_cloud.baidu import BaiduCloud
from utils import BaseObject, encodes, MyError, is_empty, is_not_empty, auto_wired, codes, ContentType, Assert, \
    validates as MyValidates, Unicode, date, str_util


class OCR(BaseObject):

    @auto_wired('utils.baidu_cloud.ocr.OCR')
    def __init__(self, api_key=None, secret_key=None, token=None, baidu_cloud=None):
        """
        百度云OCR识别
        :param api_key: 应用的API Key
        :param secret_key: 应用的Secret Key
        :param token:
        :param baidu_cloud:
        """
        if is_not_empty(token):
            self.token = token
        elif is_not_empty(api_key) and is_not_empty(secret_key):
            baidu_cloud = BaiduCloud(api_key, secret_key)
            baidu_cloud.init_token()
            self.token = baidu_cloud.token
        elif is_not_empty(baidu_cloud) and is_not_empty(baidu_cloud.token):
            self.token = baidu_cloud.token
        else:
            raise MyError('缺失鉴权 Token 参数.')

    @auto_wired('utils.baidu_cloud.ocr.OCR.bankcard')
    def bankcard(self, url, image_bs64):
        """
        银行卡OCR识别
        :param url:
        :param image_bs64:
        :return:
        """
        res = requests.post(url=url.format(access_token=self.token),
                            data={'image': image_bs64}, headers=ContentType.FORM_UTF8.value)
        res.encoding = encodes.Unicode.UTF_8.value

        print(res.status_code)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

        # if res is None or res.status_code != codes.ok:
        #     mvsi_error, errors = MvsiResultSchema(only=MvsiResultSchema().only_error()).load(res.json())
        #     Assert.is_true(is_empty(errors), errors)
        #     return mvsi_error
        # mvsi_result, errors = MvsiResultSchema(only=MvsiResultSchema().only_success()).load(res.json().get('result'))
        # Assert.is_true(is_empty(errors), errors)
        # return mvsi_result


class BankcardResult(BaseObject, db.Model):
    """
    银行卡OCR识别 响应实体
    """

    __abstract__ = True

    bank_card_number = db.Column(db.String(length=64), name='CODE', comment='银行卡卡号')


if __name__ == '__main__':
    from utils.file.img import ImgUtil
    # import datetime
    # print(datetime.datetime.strptime('12/28', '%m/%y'))

    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard?access_token={access_token}'
    ocr = OCR('h0ys8yChQt83QNxtG1UYcIfA', 'KWXy3nb75OGxP1ccIrOp7GU3gBO9rMXx')
    base_str = ImgUtil.img_compress(path='D:/AIData/6.JPG', threshold=4)
    ocr.bankcard(url, base_str)
