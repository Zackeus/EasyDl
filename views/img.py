#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : index.py 
# @Software: PyCharm
# @Time : 2019/3/21 9:50

import json
import requests
from flask import Blueprint, current_app, request

from models import FileModel, FileSchema, AppSys, AppSysSchema
from models.img import ImgDataModel, ImgDataSchema, ImgTypeModel, ImgTypeSchema

from utils import Method, ContentType, render_info, MyResponse, validated, Locations, file_to_base64, \
    Assert, is_not_empty
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
    app_sys = AppSys().dao_get_by_code(img_data.app_sys_code)  # type: AppSys

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


@img_bp.route('/loan_file/<string:id>', methods=[Method.GET.value])
@validated(ImgDataSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def get_loan(loan_file, id):
    """
    根据 ID 流水号查询贷款资料
    :param loan_file:
    :param id:
    :return:
    """
    # 查询贷款流水
    loan_file = ImgDataModel.query.get(loan_file.id)  # type: LoanFileModel
    Assert.is_true(is_not_empty(loan_file), '查无此数据', 200)
    loan_schema = ImgDataSchema().dump(loan_file)

    # 查询贷款主文件
    file = FileModel.query.get(loan_file.file_id)
    file_schema = FileSchema().dump(file)
    return render_info(MyResponse(
        msg='查询成功',
        loan_detail=loan_schema.data,
        loan_file=file_schema.data
    ))


@img_bp.route('/app_sys', methods=[Method.POST.value])
@validated(AppSysSchema, only=AppSysSchema().only_create(), consumes=ContentType.JSON.value)
def add_app_sys(app_sys):
    """
    添加应用系统
    :param AppSys app_sys:
    :return:
    """
    app_sys.dao_add()
    return render_info(MyResponse(msg='添加成功'))


@img_bp.route('/img_Type', methods=[Method.POST.value])
@validated(ImgTypeSchema, only=ImgTypeSchema().only_create(), consumes=ContentType.JSON.value)
def add_img_type(img_type):
    """
    添加图片类型
    :param ImgTypeModel img_type:
    :return: 
    """
    img_type.dao_add()
    return render_info(MyResponse(code=0, msg='添加成功'))


@img_bp.route('/push_info', methods=[Method.POST.value])
def push_info():
    print(json.dumps(request.json, indent=4, ensure_ascii=False))
    return render_info(MyResponse(msg='OK'))


if __name__ == '__main__':

    data = {
        'appId': 'zx12312hjsdfsjdkf1',
        'fileData': [
            {
                'fileName': 'pdf',
                'fileFormat': 'pdf',
                'fileBase64': file_to_base64('D:/AIData/5.pdf')
            },
            {
                'fileName': '图片',
                'fileFormat': 'jpg',
                'fileBase64': file_to_base64('D:/AIData/1.png')
            }
        ],
        'appSysCode': 'OP_LOAN_H',
        'createBy': '17037',
        'remarks': '备注信息...........',
        # 'pushUrl': 'http://127.0.0.1:5000/img/push_info'
    }

    # data = {
    #     'code': 'OP_LOAN_H',
    #     'desc': '贷后资料',
    #     'remarks': '由运营平台提交的贷后资料'
    # }

    # data = {
    #     'typeCode': 'abc',
    #     'typeExplain': '测试',
    #     'isOcr': '0',
    #     'remarks': '你大爷'
    # }

    # url = 'http://127.0.0.1:8088/loan/get_loan/2dc64710552b11e9acf95800e36a34d8'
    # res = requests.get(url=url, headers=json_headers)

    # url = 'http://127.0.0.1:8088/img/img_data'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:8088/loan/img_Type'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    #****************************************************************

    # url = 'http://10.5.60.77:8088/img/img_data'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # ****************************************************************

    url = 'http://127.0.0.1:5000/img/img_data'
    res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:5000/loan/loan_file/7358d63a590311e9affa5800e36a34d8'
    # res = requests.get(url=url, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:5000/img/app_sys'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:5000/img/img_Type'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    print(res)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))


