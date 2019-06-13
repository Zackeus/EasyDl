#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : dict_view.py 
# @Software: PyCharm
# @Time : 2019/6/12 15:12


import json
import requests
from flask import Blueprint, render_template, request, jsonify

from utils import Method, ContentType, render_info, MyResponse, validated, Locations, Assert, is_not_empty, is_empty
from utils.sys import user_util
from models import page, PageSchema
from models.sys import SysDict, SysDictSchema


dict_bp = Blueprint('dict', __name__)


@dict_bp.route('/manage', methods=[Method.GET.value])
def dict_manage():
    """
    字典管理页面
    :return:
    """
    # dicts = SysDict().dao_get_all(is_dump=True)
    #
    # if is_not_empty(dicts):
    #     dicts_data, errors = SysDictSchema().dump(dicts, many=True)
    #     Assert.is_true(is_empty(errors), errors)
    # else:
    #     dicts_data = []
    types = SysDict().dao_get_types()
    return render_info(MyResponse(msg='查询成功!', types=types), template='sys/dict/dict_manage.html')


@dict_bp.route('/page', methods=[Method.GET.value])
@validated(PageSchema, only=PageSchema().only_create(),
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
@validated(SysDictSchema, only=('type', 'description', ), page=True,
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
def dict_page(page, sys_dict):
    """
    字典分页查询
    :param page:
    :param sys_dict:
    :return:
    """
    print(page)
    print(sys_dict)
    return jsonify(MyResponse(msg='查询成功!', list=None).__dict__), 200
    # return render_info(MyResponse(msg='查询成功!', list=None))
