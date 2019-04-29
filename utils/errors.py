#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 自定义异常
# @Author : Zackeus
# @File : my_error.py 
# @Software: PyCharm
# @Time : 2019/3/22 10:15


from utils.request import codes


class MyError(Exception):

    def __init__(self, msg, code=codes.server_error, **kwargs):
        """
        自定义异常基类
        :param code: 异常代号
        :param msg: 异常信息
        :param args:
        """
        super().__init__(self)
        self.code = str(code)
        self.msg = msg
        if kwargs:
            self.kwargs = kwargs

    def __str__(self):
        return self.msg


class ConstError(TypeError):

    def __init__(self, msg):
        """
        常量异常
        :param msg:
        """
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg
