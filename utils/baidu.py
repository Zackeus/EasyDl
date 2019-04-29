#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 百度工具类
# @Author : Zackeus
# @File : baidu.py 
# @Software: PyCharm
# @Time : 2019/4/4 11:06


import requests
import json
from utils.errors import MyError
from utils.encodes import Unicode
from utils.file.img import ImgUtil
from utils.request import codes, ContentType
from utils.object_util import is_not_empty
from marshmallow import Schema, fields, post_load


class BaiduCloud(object):

    _TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
            'client_id={api_key}&client_secret={secret_key}'

    def __init__(self, api_key, secret_key):
        """

        :param api_key: 应用的API Key
        :param secret_key: 应用的Secret Key
        """
        self.token = None
        self.api_key = api_key
        self.secret_key = secret_key
        self.token_url = self._TOKEN_URL.format(api_key=self.api_key, secret_key=self.secret_key)

    def init_token(self):
        """
        百度云鉴权接口
        :return:
        :rtype:Token
        """
        res = requests.post(url=self.token_url, headers=ContentType.JSON_UTF8.value)
        res.encoding = Unicode.UTF_8.value
        if res is None or res.status_code != codes.ok:
            raise MyError(
                code=codes.server_error,
                msg='百度云鉴权请求失败【{0}】'.
                    format(res.status_code if res is not None else codes.bad)
            )
        token, _ = Token.TokenSchema().load(res.json())
        if is_not_empty(token.error):
            raise MyError(
                code=codes.server_error,
                msg='百度云鉴权失败【{0}】: {1}'.format(token.error, token.error_description)
            )
        self.token = token.access_token
        return token

    def img_class(self, url, image_bs64, top_num=5):
        """
        图片分类
        :param url: 分类接口地址
        :param image_bs64:图片base64数据
        :param top_num:返回概率最高的分类数目
        :return:
        :rtype: CategoryInfo
        """
        url = url.format(access_token=self.token)
        params = {
            'image': image_bs64,
            'top_num': top_num
        }
        res = requests.post(url=url, data=json.dumps(obj=params), headers=ContentType.JSON_UTF8.value)
        res.encoding = Unicode.UTF_8.value
        if res is None or res.status_code != codes.ok:
            return CategoryInfo(
                error_code=res.status_code if res is not None else codes.bad,
                error_msg='图片分类请求失败'
            )
        info, _ = CategoryInfo.CategoryInfoSchema().load(res.json())
        return info


class Token(object):

    def __init__(self, access_token=None, expires_in=0, refresh_token=None, scope=None, session_key=None,
                 session_secret=None, error=None, error_description=None):
        """
        百度云应用 Token 实体
        :param access_token:
        :param expires_in:有效期(秒为单位，一般为1个月)
        :param refresh_token:
        :param scope:
        :param session_key:
        :param session_secret:
        :param error:错误码
        :param error_description:错误描述信息
        """
        self.access_token = access_token
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.scope = scope
        self.session_key = session_key
        self.session_secret = session_secret
        self.error = error
        self.error_description = error_description

    class TokenSchema(Schema):

        access_token = fields.Str()
        expires_in = fields.Integer()
        refresh_token = fields.Str()
        scope = fields.Str()
        session_key = fields.Str()
        session_secret = fields.Str()
        error = fields.Str()
        error_description = fields.Str()

        @post_load
        def make_object(self, data):
            return Token(**data)


class Results(object):

    def __init__(self, name=None, score=None):
        """
        分类响应信息
        :param name: 分类名称
        :param score: 置信度
        """
        self.name = name
        self.score = score


class ResultsSchema(Schema):
    name = fields.Str()
    score = fields.Float()

    @post_load
    def make_object(self, data):
        return Results(**data)


class CategoryInfo(object):

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
        results = fields.Nested(ResultsSchema, many=True)
        error_code = fields.Integer()
        error_msg = fields.Str()

        @post_load
        def make_object(self, data):
            return CategoryInfo(**data)


if __name__ == '__main__':
    # cf = ConfigUtils(path='./config/EasyDl.cfg')
    # sections = cf.get_sections()
    # url = cf.get_key_value(section=sections[6], option='url')
    #
    # token = BaiduCloud.get_token()
    # if token is None or hasattr(token, 'error'):
    #     print('获取失败: ', token.error_description)
    # else:
    #     print(json.dumps(obj=token.__dict__, sort_keys=True, indent=2))
    #
    # base_str = ImgUtil.img_compress(path='D:/AIData/2.png')
    #
    # class_res = BaiduCloud.img_class(access_token=token.access_token,
    #                                  image_bs64=base_str,
    #                                  url=url)
    # if class_res is None or hasattr(class_res, 'error_code'):
    #     # 【17】【Open api daily request limit reached】 调用达到上限
    #     if class_res.error_code == 17:
    #         print('调用次数限制')
    #     print('分类失败: 【{0}】【{1}】'.format(class_res.error_code, class_res.error_msg))
    # else:
    #     print(json.dumps(obj=class_res.__dict__, sort_keys=True, indent=2))
    #
    # if class_res.results[0].get('score') > 0.56:
    #     print('可信')
    # else:
    #     print('不可信')
    # print(class_res.results[0])

    baidu = BaiduCloud('ijGkwuoHcLtEYsmd32C0R2ga', 'eVGhrdZhfLRbVTHvHuZM19vHOAlbYfx6')
    baidu.init_token()

    base_str = ImgUtil.img_compress(path='D:/贷后资料/b268d5945a6211e98c1d5800e36a34d8/IMG/3.PNG')
    info = baidu.img_class(
        'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/post_loan?access_token={access_token}',
        base_str
    )
    print(info.error_code)
    for r in info.results:
        print(r.name, r.score)