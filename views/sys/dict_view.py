#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : dict_view.py 
# @Software: PyCharm
# @Time : 2019/6/12 15:12


from flask import Blueprint, render_template

from utils import Method, ContentType, render_info, MyResponse, validated, Locations, is_empty, is_not_empty
from models import PageSchema
from models.sys import SysDict, SysDictSchema


dict_bp = Blueprint('dict', __name__)


@dict_bp.route('', methods=[Method.POST.value])
@validated(SysDictSchema, only=SysDictSchema().only_create(), locations=(Locations.JSON.value, ),
           consumes=ContentType.JSON.value)
def add_dict(sys_dict):
    """
    字典添加
    :param SysDict sys_dict:
    :return:
    """
    sys_dict.dao_add()
    return render_info(MyResponse(msg='添加成功!'))


@dict_bp.route('', methods=[Method.DELETE.value])
@validated(SysDictSchema, only=SysDictSchema().only_delete(), consumes=ContentType.JSON.value)
def del_menu(menu):
    """
    删除系统字典
    :param menu:
    :return:
    """
    menu = SysDict().dao_get(menu.id)
    if is_not_empty(menu):
        menu.dao_delete()
    return render_info(MyResponse(msg='删除成功'))


@dict_bp.route('/manage', methods=[Method.GET.value])
def dict_manage():
    """
    字典管理页面
    :return:
    """
    types = SysDict().dao_get_types()
    return render_template('sys/dict/dict_manage.html', types=types)


@dict_bp.route('/page', methods=[Method.GET.value])
@validated(PageSchema, only=PageSchema().only_create(),
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
@validated(SysDictSchema, only=SysDictSchema().only_page(), page=True,
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
def dict_page(page, sys_dict):
    """
    字典分页查询
    :param page:
    :param SysDict sys_dict:
    :return:
    """
    page, _ = sys_dict.dao_find_page(page)
    return render_info(page)


@dict_bp.route('/add', methods=[Method.GET.value])
@dict_bp.route('/add/<string:id>', methods=[Method.GET.value])
def dict_add(id=None):
    """
    添加字典页面
    :param id:
    :return:
    """
    sys_dict = SysDict()
    if is_empty(id):
        sys_dict.sort = 10
    else:
        sys_dict = SysDict().dao_get(id)
        sys_dict.sort = 10 if is_empty(sys_dict.sort) else sys_dict.sort + 10
    return render_template('sys/dict/dict_add.html', dict=sys_dict)
