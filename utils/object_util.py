#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : object_util.py 
# @Software: PyCharm
# @Time : 2019/3/28 13:27


class BaseObject(object):
    """
    实体基类
    """

    def gat_attrs(self):
        return ', '.join('{}={}'.format(k, getattr(self, k)) for k in self.__dict__.keys())

    def __str__(self):
        return '[{}:{}]'.format(self.__class__.__name__, self.gat_attrs())

    def __repr__(self):
        import hashlib
        from utils.encodes import Unicode

        return '{0}({1})'.format(
            self.__class__.__name__,
            hashlib.md5(self.__class__.__name__.encode(encoding=Unicode.UTF_8.value)).hexdigest()
        )


def is_empty(o):
    """
    判断对象是否为空
    :param o:
    :return:
    """
    if not o:
        return True
    if isinstance(o, str):
        return o.isspace()
    if isinstance(o, list) or isinstance(o, dict) or isinstance(o, tuple):
        return not any(o)
    return False


def is_not_empty(o):
    """
    判断对象不为空
    :param o:
    :return:
    """
    return not is_empty(o)


def create_instance(module_name, class_name, *args, **kwargs):
    """
    动态创建类实例
    :param module_name: 包名
    :param class_name: 类名
    :param args:
    :param kwargs:
    :return:
    """
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj

