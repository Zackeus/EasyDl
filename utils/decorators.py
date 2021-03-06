#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 装饰器工具类
# @Author : Zackeus
# @File : decorators.py 
# @Software: PyCharm
# @Time : 2019/4/22 16:27


from threading import Thread
from functools import wraps
from marshmallow.compat import basestring
from flask import current_app
from flask_login import config, utils

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


def login_required(func):
    """
    登录保护扩展
    :param func:
    :return:
    """

    # noinspection PyProtectedMember
    @wraps(func)
    def decorated_view(*args, **kwargs):

        if not utils.request.endpoint:
            return func(*args, **kwargs)

        view = current_app.view_functions.get(utils.request.endpoint)
        dest = '%s.%s' % (view.__module__, view.__name__)

        if utils.request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif utils.request.blueprint in current_app.login_manager._exempt_blueprints:
            return func(*args, **kwargs)
        elif dest in current_app.login_manager._exempt_views:
            return func(*args, **kwargs)
        elif not utils.current_user.is_authenticated:
            # 用户未通过登录验证
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def auto_wired(key):
    """
    参数自动装配
    :param str key:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            args_tuple = args[1:]
            if is_not_empty(args_tuple):
                return func(*args, **kwargs)

            try:
                kwargs_dict = current_app.get_object_dict(key)
                kwargs_dict.update(kwargs)
                return func(*args, **kwargs_dict)
            except RuntimeError:
                # 未创建 flask 上下文，直接返回原参数
                return func(*args, **kwargs)
        return decorated_function
    return decorator


class TimeoutException(Exception):
    pass


def set_timeout(timeout):
    def decorator(func):
        @wraps(func)
        def to_do(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self, _error=None, ):
                    Thread.__init__(self)
                    self._error = _error

                def run(self):
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        self._error = e

            t = TimeLimited()
            # t.daemon = True
            t.start()

            t.join(timeout)

            if t._error:
                raise t._error

            if t.is_alive():
                raise TimeoutException('timeout for %s' % (repr(func)))
        return to_do
    return decorator



