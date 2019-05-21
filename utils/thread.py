#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : thread.py 
# @Software: PyCharm
# @Time : 2019/5/21 14:56


from threading import Thread

from utils.response import MyResponse
from utils.request import codes


class MyThread(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        """
        自定义线程类
        """
        super(self.__class__, self).__init__(group=group, target=target, name=name,
                                             args=args, kwargs=kwargs,daemon=daemon)
        self.exit_code = str(codes.success)
        self.exc_traceback = ''
        self.exception = None

    def run(self):
        try:
            super().run()
        except Exception as e:
            res = MyResponse.init_error(e)
            self.exception = e
            self.exit_code = res.code
            self.exc_traceback = res.msg





