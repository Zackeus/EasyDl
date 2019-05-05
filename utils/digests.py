#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 信息摘要工具类
# @Author : Zackeus
# @File : digests.py 
# @Software: PyCharm
# @Time : 2019/4/30 16:24


import random
from utils.object_util import is_not_empty, create_instance

SOURCE = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz123456789'


def get_key(n):
    """
    获取密钥 n 密钥长度
    :return:
    """
    c_length = int(n)

    length = len(SOURCE) - 1
    result = ''
    for i in range(c_length):
        result += SOURCE[random.randint(0, length)]
    return result


def get_salt(n):
    """
    生成随机的Byte[]作为salt.
    :param int n: byte数组的大小
    :return:
    """
    from utils.encodes import Unicode

    return bytes(get_key(n), encoding=Unicode.UTF_8.value)


def digest(input_str, salt, hash_cls, iterations):
    """
    对字符串进行散列, 支持md5与sha1算法.
    :param str input_str: 待散列字符
    :param bytes salt: 盐
    :param str hash_cls: 算法实例
    :param int iterations: 跌算次数
    :return:
    """
    from utils.encodes import Unicode

    _hash_model = 'hashlib'

    hash_instance = create_instance(_hash_model, hash_cls)
    if is_not_empty(salt):
        hash_instance.update(salt)

    hash_instance.update(bytes(input_str, encoding=Unicode.UTF_8.value))
    res = hash_instance.digest()

    for i in range(1, iterations):
        res = create_instance(_hash_model, hash_cls, res).digest()
    return res


if __name__ == '__main__':
    print(get_key(16))

