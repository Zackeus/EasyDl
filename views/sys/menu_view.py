#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : menu.py 
# @Software: PyCharm
# @Time : 2019/6/10 9:22


import json
import requests
from flask import Blueprint, render_template

from utils import Method, ContentType, render_info, MyResponse, validated, Locations, Assert, is_not_empty
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
    parent_menu = Menu().dao_get(menu.parent_id)
    Assert.is_true(is_not_empty(parent_menu), '无效的父级菜单ID：{0}'.format(menu.parent_id))
    menu.dao_add()
    return render_info(MyResponse(msg='添加成功'))


@menu_bp.route('', methods=[Method.DELETE.value])
@validated(MenuSchema, only=MenuSchema().only_delete(), consumes=ContentType.JSON.value)
def del_menu(menu):
    """
    删除系统菜单
    :param menu:
    :return:
    """
    menu = Menu().dao_get(menu.id)
    if is_not_empty(menu):
        menu.dao_delete()
    return render_info(MyResponse(msg='删除成功'))


@menu_bp.route('', methods=[Method.PUT.value])
@validated(MenuSchema, only=MenuSchema().only_put(), consumes=ContentType.JSON.value)
def put_menu(menu):
    """
    更新系统菜单
    :param menu:
    :return:
    """
    to_do_menu = Menu().dao_get(menu.id)
    Assert.is_true(is_not_empty(to_do_menu), '无效的菜单ID：{0}'.format(menu.id))
    parent_menu = Menu().dao_get(menu.parent_id)
    Assert.is_true(is_not_empty(parent_menu), '无效的父级菜单ID：{0}'.format(menu.parent_id))

    to_do_menu.dao_put(menu)
    return render_info(MyResponse(msg='更新成功'))


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


@menu_bp.route('/max_sort/<string:id>', methods=[Method.GET.value])
@validated(MenuSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ), consumes=ContentType.JSON.value)
def max_sort(menu, id):
    """
    根据 id 查询子菜单最大最大排序值
    :param menu:
    :param id:
    :return:
    """
    sort = Menu().dao_get_max_sort_by_id(menu.id)
    return render_info(MyResponse(msg='查询成功!', sort=sort))


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


@menu_bp.route('/edit/<string:id>', methods=[Method.GET.value])
def menu_edit(id):
    """
    菜单编辑页面
    :param id:
    :return:
    """
    menu = Menu().dao_get(id)
    parent_menu = Menu().dao_get(menu.parent_id)
    return render_template('sys/menu/menu_edit.html', menu=menu, parent_menu=parent_menu)


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
