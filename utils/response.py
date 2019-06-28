#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 自定义响应信息
# @Author : Zackeus
# @File : my_response.py 
# @Software: PyCharm
# @Time : 2019/3/22 10:26


from urllib.parse import urlparse, urljoin
from marshmallow import fields, Schema, post_load
from flask import request, jsonify, render_template, redirect, url_for
from jinja2.exceptions import TemplateNotFound

from utils import codes, Headers, ContentType, validates as MyValidates


class MyResponse(object):

    def __init__(self, msg, code=codes.success, **kwargs):
        """
        自定义响应信息
        :param msg: 响应信息
        :param code: 响应吗
        :param args:
        """
        self.code = str(code)
        self.msg = msg
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    @classmethod
    def init_error(cls, e):
        """
        实例化异常信息
        :param e: 异常对象
        :return:
        """
        code = e.code if hasattr(e, 'code') and e.code else codes.server_error
        msg = e.msg if hasattr(e, 'msg') else '系统异常.'
        if hasattr(e, 'kwargs') and e.kwargs:
            return cls(code=code, msg=msg, **e.kwargs)
        return cls(code=code, msg=msg)

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


class MyResponseSchema(Schema):
    __model__ = MyResponse

    class Meta:
        strict = True

    code = fields.Str(required=True, validate=MyValidates.MyLength(min=1, not_empty=False))
    msg = fields.Str(required=True, validate=MyValidates.MyLength(min=1, not_empty=False))

    @post_load
    def make_object(self, data):
        """
        序列化对象
        :param data:
        :return:
        """
        return self.__model__(**data) if self.__model__ else data


def render_info(info, template=None, status=codes.ok, **kwargs):
    """
    客户端返回信息
    :param status: 请求状态码
    :param template: 模板路径
    :param info: 信息体(字典格式)
    :type kwargs: 模板参数对象
    :return:
    """
    if codes.ok != status and hasattr(info, 'code'):
        info.code = str(status)
    if request.headers.get(Headers.CONTENT_TYPE.value) and \
            request.headers.get(Headers.CONTENT_TYPE.value) == ContentType.JSON.value:
        # 判断请求响应类型是否为 JSON
        return jsonify(info.__dict__), status
    if template:
        # 判断模板路径是否存在
        try:
            return render_template(
                template_name_or_list=template,
                info=info.__dict__,
                **kwargs
            ), status
        except TemplateNotFound:
            return render_template(
                template_name_or_list='errors/404.html',
                info=MyResponse(code=codes.server_error, msg='模板路径不存在：{0}'.format(template)).__dict__
            ), codes.not_found
    return jsonify(MyResponse(
        code=codes.not_allowed,
        msg='不支持的请求头').__dict__
    ), codes.not_allowed


def render_json(info, status=codes.ok):
    """
    客户端返回json信息
    :param status: 请求状态码
    :param info: 信息体(字典格式)
    :return:
    """
    if codes.ok != status and hasattr(info, 'code'):
        info.code = str(status)
    return jsonify(info.__dict__), status


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='sys.index', **kwargs):
    """
    重定向到指定页面
    :param default:
    :param kwargs:
    :return:
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))







