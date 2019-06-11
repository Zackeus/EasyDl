#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : menu.py 
# @Software: PyCharm
# @Time : 2019/6/10 9:22


import json
import requests
from flask import Blueprint, current_app, request, render_template
from flask_login import current_user

from utils import Method, ContentType, render_info, MyResponse, validated, Locations, file_to_base64, \
    Assert, is_not_empty, is_empty, codes
from utils.sys import user_util
from models.sys import Menu, MenuSchema


menu_bp = Blueprint('menu', __name__)


@menu_bp.route('', methods=[Method.POST.value])
@validated(MenuSchema, only=MenuSchema().only_create(), consumes=ContentType.JSON.value)
def add_menu(menu):
    """
    添加系统菜单
    :param menu:
    :return:
    """
    menu.dao_add()
    return render_info(MyResponse(msg='添加成功'))


@menu_bp.route('/<string:id>', methods=[Method.GET.value])
@validated(MenuSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ), consumes=ContentType.JSON.value)
def get_menus(menu, id):
    """
    根据父级菜单ID查询子级菜单
    :param menu:
    :param id:
    :return:
    """
    menus = user_util.get_menus_by_user(menu.id, is_dump=True)
    return render_info(MyResponse(msg='查询成功', menus=menus))


@menu_bp.route('/manage', methods=[Method.GET.value])
def menu_manage():
    """
    菜单管理页面
    :return:
    """
    menus = Menu().dao_get_all(is_dump=True)
    return render_info(MyResponse(msg='查询成功!', menus=menus), template='sys/menu/menu_manage.html')


@menu_bp.route('/add/<string:id>', methods=[Method.GET.value])
def menu_add(id):
    """
    菜单添加页面
    :param id:
    :return:
    """
    menu = Menu().dao_get(id)
    sort = Menu().dao_get_max_sort_by_id(id)
    return render_template('sys/menu/menu_add.html', menu=menu, sort=sort)


if __name__ == '__main__':

    data = {
        'parentId': '9c86ff008b3e11e98fbc5800e36a34d8',
        'name': '菜单管理',
        'icon': 'layui-icon-biaodan',
        'sort': 60,
        'href': '/sys/menu/manage',
        'spread': False,
        'createBy': '1'
    }

    url = 'http://127.0.0.1:5000/sys/menu'
    res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    print(res)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
