#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : index.py 
# @Software: PyCharm
# @Time : 2019/3/21 9:50

import json
from flask import Blueprint, current_app, request

from models.img import ImgDataModel, ImgDataSchema, ImgTypeModel, ImgTypeSchema, ImgDetailModel, ImgDetailSchema

from utils import Method, ContentType, render_info, MyResponse, validated, Locations, file_to_base64, \
    Assert, is_not_empty, is_empty, codes
from utils.file import FileUtil


img_bp = Blueprint('img', __name__)


@img_bp.route('/img_data', methods=[Method.POST.value])
@validated(ImgDataSchema, only=ImgDataSchema().only_create(), consumes=ContentType.JSON.value)
def add_img(img_data):
    """
    图片文件入库
    :param ImgDataModel img_data:
    :return:
    """
    img_data.dao_create()
    app_sys = img_data.dao_get_app_sys(img_data.app_sys_code)
    Assert.is_true(is_not_empty(app_sys), '无效的应用系统：{0}'.format(img_data.app_sys_code), codes.unprocessable)

    # 通过外键添加
    img_data.app_sys_id = app_sys.id

    # 创建资料目录
    loan_dir = FileUtil.path_join(
        current_app.config.get('DATA_DIR'),
        img_data.id
    )

    # 信息入库
    handle_info = img_data.dao_add_info(loan_dir)
    return render_info(MyResponse(msg='接收资料成功', handle_info=handle_info))


@img_bp.route('/img_data/<string:id>', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def get_img(img_data, id):
    """
    根据 ID 流水号查询图片流水(附带路径)
    :param img_data:
    :param id:
    :return:
    """
    # 查询图片流水
    img_data = ImgDataModel.query.get(img_data.id)  # type: ImgDataModel
    Assert.is_true(is_not_empty(img_data), '查无此数据', codes.no_data)
    img_data_dict, errors = ImgDataSchema().dump(img_data)
    Assert.is_true(is_empty(errors), errors)

    # 过滤图片明细字典字段
    ImgDataSchema().filter_img_details(img_data_dict.get('imgDetails', []), ['fileData'])
    return render_info(MyResponse(
        msg='查询成功',
        img_data=img_data_dict
    ))


@img_bp.route('/img_detail/type', methods=[Method.PATCH.value])
@validated(ImgDetailSchema, only=ImgDetailSchema().only_patch_type(), consumes=ContentType.JSON.value)
def patch_img_detail_type(img_detail):
    """
    更新图片明细类型
    :param ImgDetailModel img_detail:
    :return:
    """
    img_type = ImgTypeModel().dao_get_by_code(img_detail.img_type_code)
    Assert.is_true(is_not_empty(img_type), '无效的图片类型：{0}'.format(img_detail.img_type_code), codes.unprocessable)

    img_detail_id = img_detail.id
    # 接口提交的更新者
    update_by = img_detail.update_by
    img_detail = ImgDetailModel().dao_get(img_detail_id)  # type: ImgDetailModel
    Assert.is_true(is_not_empty(img_detail), '无查无此数据：{0}'.format(img_detail_id), codes.no_data)

    img_detail.update_by = update_by
    img_detail.dao_update_type(img_type.id)
    return render_info(MyResponse('更新成功'))


@img_bp.route('/img_Type', methods=[Method.POST.value])
@validated(ImgTypeSchema, only=ImgTypeSchema().only_create(), consumes=ContentType.JSON.value)
def add_img_type(img_type):
    """
    添加图片类型
    :param ImgTypeModel img_type:
    :return: 
    """
    img_type.dao_add()
    return render_info(MyResponse('添加成功'))


@img_bp.route('/push_info', methods=[Method.POST.value])
def push_info():
    print(json.dumps(request.json, indent=4, ensure_ascii=False))
    return render_info(MyResponse('OK'))


