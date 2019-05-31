#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 自定义校验
# @Author : Zackeus
# @File : parser.py 
# @Software: PyCharm
# @Time : 2019/3/25 15:49


import utils
import requests
from webargs.flaskparser import FlaskParser
from werkzeug.exceptions import MethodNotAllowed
from marshmallow.validate import Length, ValidationError
from enum import Enum, unique


@unique
class Locations(Enum):
    """
    参数请求地点
    """
    QUERY = 'query'
    QUERY_STRING = 'querystring'
    JSON = 'json'
    FORM = 'form'
    HEADERS = 'headers'
    COOKIES = 'cookies'
    FILES = 'files'
    VIEW_ARGS = 'view_args'


class Parser(FlaskParser):

    # 校验错误码 422
    DEFAULT_VALIDATION_STATUS = requests.codes.unprocessable

    def validated(self, schema_cls, only=None, locations=(Locations.JSON.value, ),
                  schema_kwargs=None, consumes=None, **kwargs):
        """
        参数校验器
        :param schema_cls: 校验 schema 类
        :param tuple|list only: 参数校验白名单，如果为None，则校验全部字段
        :param tuple locations: 搜索值的请求位置
        :param schema_kwargs:
        :param consumes: 请求处理类型
        :param kwargs:
        :return:
        """
        schema_kwargs = schema_kwargs or {}

        def factory(request):
            if consumes and request.headers.get(utils.Headers.CONTENT_TYPE.value, '') != consumes:
                # 请求头校验
                raise MethodNotAllowed(description='不支持的请求头')
            return schema_cls(
                only=only,
                partial=False,
                strict=True,
                context={"request": request},
                **schema_kwargs
            )

        return self.use_args(factory, locations=locations, **kwargs)


class MyLength(Length):
    """
    长度校验
    """
    message_not_empty = '不能为空.'
    __encodes = [
        utils.encodes.Unicode.UTF_8.value,
        utils.encodes.Unicode.GBK.value
    ]

    def __init__(self, min=None, max=None, error=None, equal=None, not_empty=True, encode_str=None):
        """

        :param int min:
        :param int max:
        :param error:
        :param equal:
        :param bool not_empty: 是否允许为空
        :param str encode_str:
        """

        super(MyLength, self).__init__(min, max, error, equal)
        self.not_empty = not_empty
        self.encode_str = encode_str

    def __call__(self, value):
        super().__call__(value)

        if not self.not_empty and utils.is_empty(value):
            raise ValidationError(self.message_not_empty)

        if utils.is_not_empty(self.encode_str):
            utils.Assert.is_true(self.encode_str in self.__encodes, '无效的编码{0}'.format(self.encode_str))

            encode_len = len(str(value).encode(self.encode_str))

            if self.min is not None and encode_len < self.min:
                message = self.message_min if self.max is None else self.message_all
                raise ValidationError(self._format_error(value, message))

            if self.max is not None and encode_len > self.max:
                message = self.message_max if self.min is None else self.message_all
                raise ValidationError(self._format_error(value, message))

        return value


parser = Parser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
validated = parser.validated


