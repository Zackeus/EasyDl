#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : num_util.py 
# @Software: PyCharm
# @Time : 2019/5/28 10:18


def is_odd(n):
    """
    是否为奇数
    :param n:
    :return:
    """
    n = int(n)
    if (n % 2) == 0:
        return False
    return True


def is_even(n):
    """
    是否为偶数
    :param n: 
    :return: 
    """
    n = int(n)
    if (n % 2) == 0:
        return True
    return False
