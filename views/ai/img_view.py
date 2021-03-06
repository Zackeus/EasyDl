#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : index.py 
# @Software: PyCharm
# @Time : 2019/3/21 9:50

from flask import Blueprint, render_template, url_for

from models import PageSchema, FlowInfo, FlowInfoSchema
from models.img import ImgDataModel, ImgDataSchema, ImgDetailModel, ImgDetailSchema

from utils import Method, ContentType, render_info, validated, Locations, Assert, \
    is_empty, is_not_empty, codes, MyResponse
from utils.sys import get_app_sys_types
from utils.file import FileFormat


img_bp = Blueprint('img', __name__)


@img_bp.route('/img_data/<string:id>', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def get_img_data(img_data, id):
    """
    图片流水查询
    :param img_data:
    :param id:
    :return:
    """
    # 查询图片流水
    img_data = ImgDataModel().dao_get(img_data.id)  # type: ImgDataModel
    Assert.is_true(is_not_empty(img_data), '查无此数据', codes.no_data)
    img_data_dict, errors = ImgDataSchema(only=ImgDataSchema().dump_only_get()).dump(img_data)
    Assert.is_true(is_empty(errors), errors)
    return render_info(MyResponse(msg='查询成功', imgData=img_data_dict))


@img_bp.route('/img_datas.html', methods=[Method.GET.value])
def img_data_html():
    """
    图像识别管理页面
    :return:
    """
    app_sys_types = get_app_sys_types()
    return render_template('ai/img/img_datas.html', app_sys_types=app_sys_types)


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


@img_bp.route('/img_files/flow_page/<string:id>.html', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def img_files_html(img_data, id):
    """
    图片文件流加载页面
    :param img_data:
    :param id: 图片流水号
    :return:
    """
    return render_template('ai/img/img_files_flow_page.html', img_data_id=img_data.id)


@img_bp.route('/img_files/flow_page', methods=[Method.GET.value])
@validated(PageSchema, only=PageSchema().only_create(),
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
@validated(ImgDetailSchema, only=ImgDetailSchema().only_flow_page(), page=True,
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
def img_files_flow_page(page, img_detail):
    """
    图片文件流加载
    :param page:
    :param img_detail:
    :return:
    """
    page, pagination = img_detail.dao_find_page(page)

    flow_img_details = []
    for img_detail in pagination.items:
        url = url_for('file.file_download', id=img_detail.file_id, md5_id=img_detail.file_md5)
        if not img_detail.is_handle:
            alt = '待处理'
        elif is_not_empty(img_detail.img_type):
            alt = img_detail.img_type.type_explain
        else:
            alt = img_detail.err_msg
        flow_info = FlowInfo(url, url, alt, img_detail.file_id)
        flow_img_details.append(flow_info)

    flow_img_details_dict, errors = FlowInfoSchema().dump(flow_img_details, many=True)
    Assert.is_true(is_empty(errors), errors)

    page_dict, page_errors = PageSchema().dump(page)
    Assert.is_true(is_empty(page_errors), page_errors)
    page_dict['data'] = flow_img_details_dict

    return render_info(page_dict)


@img_bp.route('/img_source_files/flow_page/<string:id>.html', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def img_source_files_html(img_data, id):
    """
    源文件流加载页面
    :param img_data:
    :param id: 图片流水号
    :return:
    """
    return render_template('ai/img/img_source_files_flow_page.html', img_data_id=img_data.id)


@img_bp.route('/img_source_files/flow_page/<string:id>', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ),
           consumes=ContentType.JSON.value)
def img_source_files_flow_page(img_data, id):
    """
    源文件流加载
    :param img_data:
    :param id:
    :return:
    """
    source_files = img_data.dao_get_source_files(img_data.id)
    Assert.is_true(is_not_empty(source_files), '查无此数据', codes.no_data)

    file_datas = []
    for source_file in source_files:
        url = url_for('file.file_download', id=source_file.id, md5_id=source_file.md5_id)
        if source_file.file_format.upper() == FileFormat.PDF.value:
            url = url + '/' + source_file.id
        flow_info = FlowInfo(url, url, source_file.file_name, source_file.id, source_file.file_format)
        file_datas.append(flow_info)

    file_datas_dict, errors = FlowInfoSchema().dump(file_datas, many=True)
    Assert.is_true(is_empty(errors), errors)
    return render_info(MyResponse('查询成功', data=file_datas_dict))


@img_bp.route('/files_handle/<string:id>.html', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def files_handle_html(img_data, id):
    """
    文件处理页面
    :param img_data:
    :param id: 图片流水号
    :return:
    """
    source_files = img_data.dao_get_source_files(img_data.id)
    Assert.is_true(is_not_empty(source_files), '查无此数据', codes.no_data)

    for source_file in source_files:
        children = ImgDetailModel().dao_get_children(source_file.id)
        source_file.img_page = 0 if is_empty(children) else len(children)
    return render_template('ai/img/files_handle.html', img_data_id=img_data.id, source_files=source_files)


@img_bp.route('/files_handle/flow_page', methods=[Method.GET.value])
@validated(PageSchema, only=PageSchema().only_create(),
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
@validated(ImgDetailSchema, only=ImgDetailSchema().only_flow_page(), page=True,
           locations=(Locations.PAGE.value, ), consumes=ContentType.JSON.value)
def files_handle_flow_page(page, img_detail):
    """
    文件处理流加载
    :param page:
    :param img_detail:
    :return:
    """
    page, pagination = img_detail.dao_find_page(page)

    flow_img_details = []
    for img_detail in pagination.items:
        url = url_for('file.file_download', id=img_detail.file_id, md5_id=img_detail.file_md5)
        if not img_detail.is_handle:
            alt = '待处理'
        elif is_not_empty(img_detail.img_type):
            alt = img_detail.img_type.type_explain
        else:
            alt = img_detail.err_msg
        flow_info = FlowInfo(url, url, alt, img_detail.parent_file_id)
        flow_img_details.append(flow_info)

    flow_img_details_dict, errors = FlowInfoSchema().dump(flow_img_details, many=True)
    Assert.is_true(is_empty(errors), errors)

    page_dict, page_errors = PageSchema().dump(page)
    Assert.is_true(is_empty(page_errors), page_errors)
    page_dict['data'] = flow_img_details_dict

    return render_info(page_dict)





