#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : xunfei.py 
# @Software: PyCharm
# @Time : 2019/5/21 10:02


import time
import hashlib
import hmac
import base64

from utils.object_util import BaseObject


class Sign(BaseObject):

    def __init__(self, app_id, api_key):
        """
        讯飞开放平台数字签名
        :param str app_id: 讯飞开放平台应用ID
        :param str api_key: 讯飞开放平台应用秘钥
        """
        self.app_id = app_id
        # 当前时间戳
        self.ts = str(int(time.time()))
        self.base_string = self._generate_base_string()
        self.signa = self._hmac_sha1(api_key)

    def _generate_base_string(self):
        """
        app_id和当前时间戳ts拼接 base_string
        :return:
        """
        from utils import encodes
        hl = hashlib.md5()
        hl.update((self.app_id + self.ts).encode(encodes.Unicode.UTF_8.value))
        base_string = hl.hexdigest()
        return base_string.encode(encodes.Unicode.UTF_8.value)

    def _hmac_sha1(self, api_key):
        """
        对 base_string 进行 hmac_sha1 加密
        :param api_key: 讯飞开放平台应用秘钥
        :return:
        """
        from utils import encodes
        signa = hmac.new(api_key.encode(encodes.Unicode.UTF_8.value), self.base_string, hashlib.sha1).digest()
        signa = base64.b64encode(signa).decode(encodes.Unicode.UTF_8.value)
        return signa


if __name__ == '__main__':
    sign = Sign('5b331864', '8ce5edee08cdce711d08fea808d55b00')
    print(sign.signa)






