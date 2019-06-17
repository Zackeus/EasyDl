#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : index.py 
# @Software: PyCharm
# @Time : 2019/3/21 9:50

from flask import Blueprint, render_template

from models import PageSchema
from models.img import ImgDataSchema

from utils import Method, ContentType, render_info, validated, Locations
from utils.sys import get_app_sys_types


img_bp = Blueprint('img', __name__)


@img_bp.route('/img_data/manage', methods=[Method.GET.value])
def img_data_manage():
    """
    图像识别管理页面
    :return:
    """
    app_sys_types = get_app_sys_types()
    return render_template('ai/img/img_data_manage.html', app_sys_types=app_sys_types)


@img_bp.route('/img_data/page', methods=[Method.GET.value])
@validated(PageSchema, only=PageSchema().only_create(),
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
@validated(ImgDataSchema, only=ImgDataSchema().only_page(), page=True,
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
def img_data_page(page, img_data):
    """
    图像流水分页查询
    :param page:
    :param img_data:
    :return:
    """
    page, _ = img_data.dao_find_page(page)
    return render_info(page)


