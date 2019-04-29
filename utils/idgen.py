#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 成唯一性ID算法的工具类
# @Author : Zackeus
# @File : idgen.py 
# @Software: PyCharm
# @Time : 2019/3/26 15:24


import uuid


class IdGen(object):

    @staticmethod
    def uuid():
        """
        uuid, 无-分割
        :return:
        """
        return str(uuid.uuid1()).replace('-', '')


if __name__ == '__main__':
    print(len(IdGen.uuid()))