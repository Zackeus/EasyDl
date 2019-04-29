#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 装饰器工具类
# @Author : Zackeus
# @File : decorators.py 
# @Software: PyCharm
# @Time : 2019/4/22 16:27


from functools import wraps
from marshmallow.compat import basestring

from utils.str_util import Dict
from utils.object_util import is_not_empty, create_instance
from utils.errors import MyError


def result_mapper(schema_cls, module_name=None, *s, **ks):
    """
    db 结果映射器
    :param module_name: 包名
    :param schema_cls: 类实例/类字符名（当为字符时，会根据字符和包名实例化类）
    :return:
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # 根据参数类型实例化序列化实例
            cls = schema_cls
            if isinstance(cls, type):
                cls = cls(*s, **ks)
            elif isinstance(cls, basestring):
                cls = create_instance(module_name, cls, *s, **ks)

            keys, res = func(*args, **kwargs)

            if not res:
                return res

            # 查询转字典
            res_add = Dict(dict(zip(keys, res)))
            res_dic = res_add.load_nest()

            # 字典反序列化
            entity, errors = cls.load(res_dic, partial=cls.partial_db())

            if is_not_empty(errors):
                raise MyError(msg=errors)
            return entity
        return decorated_function
    return decorator

