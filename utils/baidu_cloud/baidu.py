#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : baidu.py 
# @Software: PyCharm
# @Time : 2019/5/14 11:08


import requests

from utils import encodes
from utils.errors import MyError
from utils.request import codes, ContentType
from utils.object_util import is_not_empty, BaseObject
from marshmallow import Schema, fields, post_load


class BaiduCloud(BaseObject):

    _TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
            'client_id={api_key}&client_secret={secret_key}'

    def __init__(self, api_key, secret_key):
        """
        百度云应用鉴权对象
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
        res.encoding = encodes.Unicode.UTF_8.value
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


class Token(BaseObject):

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
