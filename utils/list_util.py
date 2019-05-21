#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : list.py 
# @Software: PyCharm
# @Time : 2019/5/21 13:47

import math


def split_list(ls, n):
    """
    分割列表
    :param ls: 待分割列表
    :param n: 分割列表数
    :return:
    """
    res = []
    length = len(ls)
    for i in range(n):
        one_list = ls[math.floor(i / n * length):math.floor((i + 1) / n * length)]
        res.append(one_list)
    return res


if __name__ == '__main__':
    print(split_list([1, 2, 3, 4, 5, 6, 7, 8], 3))
