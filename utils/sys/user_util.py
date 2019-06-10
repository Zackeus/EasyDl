#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : user_util.py 
# @Software: PyCharm
# @Time : 2019/6/10 8:52


from flask_login import current_user

from models.sys import Menu


def get_tree_menus_by_user():
    """
    获取用户授权树形菜单
    :return:
    """
    if current_user.is_admin:
        return Menu().dao_get_all_tree_menus()
    return []


def get_menus_by_user(id):
    """
    获取用户授权左侧菜单
    :param id: 一级菜单ID
    :return:
    """
    if current_user.is_admin:
        return Menu().dao_get_all_menus(id)
    return []
