#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : huawei.py 
# @Software: PyCharm
# @Time : 2019/8/26 9:13

import json
import requests

from utils import encodes, MyError, codes, ContentType
from utils.object_util import BaseObject


class HuaweiCloud(BaseObject):

    _TOKEN_URL = 'https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens'

    def __init__(self, user_name, password, domain_name):
        """
        华为云应用鉴权对象
        :param user_name: 用户名称，根据获取token的主体填写
        :param password: 用户的登录密码
        :param domain_name: 用户所属的账号名称。如果是账号获取token，账号的user.name和domain.name相同
        """
        self.token = None
        self.user_name = user_name
        self.password = password
        self.domain_name = domain_name

    def init_token(self):
        """
        华为云鉴权接口
        :return:
        """
        token_data = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': self.user_name,
                            'password': self.password,
                            'domain': {'name': self.domain_name}
                        }
                    }
                },
                'scope': {
                    'project': {'name': 'cn-north-1'}
                }
            }
        }

        res = requests.post(url=self._TOKEN_URL, data=json.dumps(obj=token_data), headers=ContentType.JSON_UTF8.value)
        res.encoding = encodes.Unicode.UTF_8.value
        if res is None or res.status_code != codes.huawei_token_success:
            raise MyError(
                code=codes.server_error,
                msg='华为云鉴权请求失败【{0}】'.
                    format(res.status_code if res is not None else codes.bad)
            )
        self.token = res.headers['X-Subject-Token']