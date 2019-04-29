#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 断言工具类
# @Author : Zackeus
# @File : my_assert.py
# @Software: PyCharm
# @Time : 2019/3/26 9:46


import requests
from utils.errors import MyError


class Assert(object):

    @staticmethod
    def is_true(assert_condition, assert_msg='系统异常...', assert_code=requests.codes.server_error):
        """
        断言条件是否为真，为假则抛出异常
        :param assert_condition:断言条件
        :param assert_msg:断言信息
        :param assert_code:断言code
        :return:
        """
        if not assert_condition:
            raise MyError(code=assert_code, msg=assert_msg)


if __name__ == '__main__':
    a = 10
    Assert.is_true(assert_condition=a > 9)
