#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : index.py 
# @Software: PyCharm
# @Time : 2019/3/21 9:50

from flask import Blueprint, render_template, url_for, jsonify

from models import PageSchema
from models.img import ImgDataSchema

from utils import Method, ContentType, render_info, validated, Locations
from utils.sys import get_app_sys_types


img_bp = Blueprint('img', __name__)


@img_bp.route('/img_data/<string:id>', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def get_img_data(img_data, id):
    """
    根据流水号查询明细
    :param img_data:
    :param id:
    :return:
    """
    print(img_data)
    return render_template('ai/img/images.html')


@img_bp.route('/img_datas', methods=[Method.GET.value])
def get_img_datas():
    img_datas = []

    for i in range(1, 17):
        data = {
            'src': url_for('static', filename='images/test/{0}.PNG'.format(i)),
            'thumb': url_for('static', filename='images/test/{0}.PNG'.format(i)),
            'alt': '贷后资料{0}'.format(i),
            'pid': i
        }
        img_datas.append(data)
    return jsonify(img_datas)


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





