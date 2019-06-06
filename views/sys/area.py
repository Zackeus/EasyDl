#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 系统页面
# @Author : Zackeus
# @File : area.py 
# @Software: PyCharm
# @Time : 2019/5/6 13:26


from flask import Blueprint, render_template
from flask_login import current_user

from utils.request import Method

area_bp = Blueprint('sys', __name__)


@area_bp.route('/index', methods=[Method.GET.value])
def index():
    """
    主页面
    :return:
    """
    print(current_user)
    print(current_user.is_admin)
    return render_template(template_name_or_list='sys/index.html')


@area_bp.route('/main', methods=[Method.GET.value])
def main():
    """
    子页面
    :return:
    """
    return render_template(template_name_or_list='sys/main.html')



