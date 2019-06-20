#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : index.py 
# @Software: PyCharm
# @Time : 2019/3/21 9:50

from flask import Blueprint, render_template, url_for

from models import PageSchema
from models.img import ImgDataModel, ImgDataSchema

from utils import Method, ContentType, render_info, validated, Locations, Assert, is_not_empty, codes, MyResponse
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


@img_bp.route('/img_files/manage/<string:id>', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def img_files_manage(img_data, id):
    """
    图片文件管理
    :param img_data:
    :param id: 图片流水号
    :return:
    """
    print(img_data)
    return render_template('ai/img/img_files_manage.html', img_data_id=img_data.id)


@img_bp.route('/img_files/<string:id>', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ),
           consumes=ContentType.JSON.value)
def img_files(img_data, id):
    """
    图片文件浏览
    :param img_data:
    :param id:
    :return:
    """
    img_data = ImgDataModel().dao_get(img_data.id)  # type: ImgDataModel
    Assert.is_true(is_not_empty(img_data), '查无此数据', codes.no_data)

    img_datas = []
    for img_detail in img_data.img_details:
        url = url_for('file.file_download', id=img_detail.file_id, md5_id=img_detail.file_md5)
        if not img_detail.is_handle:
            alt = '待处理'
        elif is_not_empty(img_detail.img_type):
            alt = img_detail.img_type.type_explain
        else:
            alt = img_detail.err_msg
        data = {
            'src': url,
            'thumb': url,
            'alt': alt,
            'pid': img_detail.file_id
        }
        img_datas.append(data)
    return render_info(MyResponse('查询成功', data=img_datas))





