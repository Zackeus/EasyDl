#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : image.py 
# @Software: PyCharm
# @Time : 2019/5/14 11:10


import requests
import json
from marshmallow import Schema, fields, post_load

from utils import encodes
from utils.errors import MyError
from utils.file.img import ImgUtil
from utils.request import codes, ContentType
from utils.object_util import is_not_empty, BaseObject
from utils.baidu_cloud.baidu import BaiduCloud
from utils.decorators import auto_wired


class Image(BaseObject):

    @auto_wired('utils.baidu_cloud.image.Image')
    def __init__(self, api_key=None, secret_key=None, baidu_cloud=None):
        """
        百度云图像识别
        :param str api_key: 应用的API Key
        :param str secret_key: 应用的Secret Key
        :param BaiduCloud baidu_cloud:
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

    @auto_wired('utils.baidu_cloud.image.Image.to_class')
    def to_class(self, url, image_bs64, top_num=5):
        """
        图片分类
        :param url: 分类接口地址
        :param image_bs64: 图片base64数据
        :param top_num: 返回概率最高的分类数目
        :return:
        :rtype: CategoryInfo
        """
        url = url.format(access_token=self.token)
        params = {
            'image': image_bs64,
            'top_num': top_num
        }
        res = requests.post(url=url, data=json.dumps(obj=params), headers=ContentType.JSON_UTF8.value)
        res.encoding = encodes.Unicode.UTF_8.value
        if res is None or res.status_code != codes.ok:
            return CategoryInfo(
                error_code=res.status_code if res is not None else codes.bad,
                error_msg='图片分类请求失败'
            )
        info, _ = CategoryInfo.CategoryInfoSchema().load(res.json())
        return info


class CategoryResults(BaseObject):

    def __init__(self, name=None, score=None):
        """
        分类响应信息
        :param name: 分类名称
        :param score: 置信度
        """
        self.name = name
        self.score = score

    class CategoryResultsSchema(Schema):
        name = fields.Str()
        score = fields.Float()

        @post_load
        def make_object(self, data):
            return CategoryResults(**data)


class CategoryInfo(BaseObject):

    def __init__(self, log_id=None, results=None, error_code=None, error_msg=None):
        """
        分类响应信息
        :param log_id:唯一的log id，用于问题定位
        :param results:识别结果数组
        :param error_code:错误码
        :param error_msg:错误描述信息
        """
        self.log_id = log_id
        self.results = results
        self.error_code = error_code
        self.error_msg = error_msg

    class CategoryInfoSchema(Schema):
        log_id = fields.Integer()
        results = fields.Nested(CategoryResults.CategoryResultsSchema, many=True)
        error_code = fields.Integer()
        error_msg = fields.Str()

        @post_load
        def make_object(self, data):
            return CategoryInfo(**data)


if __name__ == '__main__':
    # baidu = BaiduCloud('ijGkwuoHcLtEYsmd32C0R2ga', 'eVGhrdZhfLRbVTHvHuZM19vHOAlbYfx6')
    # baidu.init_token()

    # image = Image(baidu_cloud=baidu)

    # 图片分类
    # image = Image('vqxa46w07EWb5UpMQuQ1pKLz', 'RPYI6LZnFSU8331umUcnA0G8bewrZjFX')
    # print(image.token)
    #
    # base_str = ImgUtil.img_compress(
    #     path='D:/FileData/11.JPG',
    #     threshold=0.5
    # )
    # print(base_str)
    # print(len(base_str))
    # info = image.to_class(
    #     'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/post_loan?access_token={access_token}',
    #     base_str
    # )
    # if is_not_empty(info.error_code):
    #     print(info.error_code)
    # else:
    #     for r in info.results:
    #         print(r.name, r.score)

    image = Image('h0ys8yChQt83QNxtG1UYcIfA', 'KWXy3nb75OGxP1ccIrOp7GU3gBO9rMXx')
    print(image.token)

    base_str = ImgUtil.img_compress(
        path='D:/AIData/OCR/22.JPG',
        threshold=0.5
    )

    print(base_str)
    print(len(base_str))

    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/vehicle_invoice?access_token={access_token}'.\
        format(access_token=image.token)
    params = {
        'image': base_str
    }

    res = requests.post(url=url, data=params, headers=ContentType.FORM_UTF8.value)
    res.encoding = encodes.Unicode.UTF_8.value

    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))

