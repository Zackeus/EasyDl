#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 字符工具类
# @Author : Zackeus
# @File : string.py 
# @Software: PyCharm
# @Time : 2019/3/27 9:22


import decimal
import json
import datetime
from addict import Dict as BasicDict
from utils.object_util import is_empty, is_not_empty

UNDER_LINE = '_'


def abb_str(s, length=64, suffix='***'):
    """
    将字符缩略到指定长度
    :param s: 待缩略字符
    :param length: 缩略长度
    :param suffix: 缩略后缀
    :return:
    """
    if not isinstance(s, str):
        s = str(s)
    if len(s) > length:
        s = s[:(length - len(suffix))] + suffix
    return s


def get_dict_value(date, keys, default=None):
    """
    通过（key1.key2.key3）形式获取嵌套字典值
    :param date:
    :param keys:
    :param default:
    :return:
    """
    # default=None，在key值不存在的情况下，返回None
    keys_list = keys.split('.')
    if isinstance(date, dict):
        dictionary = dict(date)
        for i in keys_list:
            dict_values = default
            if dictionary.get(i) is not None:
                dict_values = dictionary.get(i)
            elif dictionary.get(i) is None:
                # 如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
                dict_values = dictionary.get(int(i))
            dictionary = dict_values
        return dictionary
    else:
        dictionary = dict(eval(date))
        # 如果传入的字符串数据格式为字典格式，转字典类型，不然返回None
        if isinstance(dictionary, dict):
            for i in keys_list:
                dict_values = default
                if dictionary.get(i) is not None:
                    dict_values = dictionary.get(i)
                elif dictionary.get(i) is None:
                    # 如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
                    dict_values = dictionary.get(int(i))
                dictionary = dict_values
            return dictionary


# noinspection PyBroadException
def amount_formatting(s, formats):
    """
    金额格式化
    :param s:
    :param formats:
    :return:
    """
    try:
        if is_not_empty(s):
            for format in formats:
                s = s.replace(format, '')
            return float(s.strip())
        return None
    except:
        return None


class Dict(BasicDict):
    """
    dict 扩展, 支持 key1.key2.key3 的形式解析字典
    """

    def load_nest(self):
        """
        多层嵌套解析
        :return:
        """
        import os

        d2 = {}
        for key, value in self.items():
            # 键值转字符 ，解决反序列化时类型异常问题
            value = str(value)
            if os.curdir in key:
                parts = key.split(os.curdir)
                par = d2
                key = parts.pop(0)
                while parts:
                    par = par.setdefault(key, {})
                    key = parts.pop(0)
                par[key] = value
            else:
                d2[key] = value
        return d2


class DateEncoder(json.JSONEncoder):
    """
    重写构造json类，遇到日期特殊处理，其余的用内置
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


class DecimalEncoder(json.JSONEncoder):
    """
    重写构造json类，遇到日期特殊处理，其余的用内置
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        else:
            return json.JSONEncoder.default(self, o)


class EncodingFormat(object):

    @classmethod
    def l_trim(cls, haystack, left=''):
        if is_empty(haystack):
            return haystack
        elif is_empty(left):
            return haystack.lstrip()
        else:
            return haystack.lstrip(left)

    @classmethod
    def pep8_to_hump(cls, s, separator=UNDER_LINE):
        """
         pep8 格式字符转驼峰
         step1.原字符串转小写,原字符串中的分隔符用空格替换,在字符串开头加上分隔符
         step2.将字符串中每个单词的首字母转换为大写,再去空格,去字符串首部附加的分隔符
        :param s:
        :param separator:
        :return:
        """
        import string
        s = separator + s.lower().replace(separator, ' ')
        return cls.l_trim(string.capwords(s).replace(' ', ''), separator)

    @classmethod
    def hump_to_pep8(cls, s):
        """
         驼峰命名转 pep8
         小写和大写紧挨一起的地方,加上分隔符,然后全部转小写
        :param s:
        :return:
        """
        if is_empty(s):
            return s
        res = s[0]
        for i in range(1, len(s)):
            # s[i] 直接copy 或 先加'_'再copy
            if s[i].isupper() and not s[i - 1].isupper():  # 加'_',当前为大写，前一个字母为小写
                res += UNDER_LINE
                res += s[i]
            elif s[i].isupper() and s[i - 1].isupper() and s[i + 1].islower():
                # 加'_',当前为大写，前一个字母为小写
                res += UNDER_LINE
                res += s[i]
            else:
                res += s[i]
        return res.lower()


if __name__ == '__main__':
    data = {'a': {'b': {'c': '你大爷'}}}
    print(get_dict_value(data, 'a.b.c'))




