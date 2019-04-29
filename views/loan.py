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

from models.file import FileModel, FileSchema
from models.loan.loan_file import LoanFileModel, LoanFileSchema
from models.loan.loan_type import LoanTypeModel, LoanTypeSchema
from models.loan.flow_type import FlowTypeModel, FlowTypeSchema
from models.loan.img_type import ImgTypeModel, ImgTypeSchema
from utils.request import Method, ContentType
from utils.response import render_info, MyResponse
from utils.validates import validated, Locations
from utils.encodes import file_to_base64
from utils.assert_util import Assert
from utils.object_util import is_not_empty
from utils.file.file import FileUtil


loan_bp = Blueprint('loan', __name__)


@loan_bp.route('/loan_file', methods=[Method.POST.value])
@validated(LoanFileSchema, only=LoanFileSchema().only_create(), consumes=ContentType.JSON.value)
def add_loan(loan_file):
    """
    贷款文件入库
    :type loan_file: LoanFileModel
    :param loan_file:
    :return:
    """
    loan_file.dao_create()
    loan_type = LoanTypeModel().dao_get_by_type(loan_file.loan_type.loan_type_name)  # type: LoanTypeModel
    flow_type = FlowTypeModel().dao_get_by_type(loan_file.flow_type.flow_type_name)  # type: FlowTypeModel

    # 删除关联，通过外键添加
    del loan_file.loan_type
    loan_file.loan_type_id = loan_type.id
    del loan_file.flow_type
    loan_file.flow_type_id = flow_type.id

    # 创建资料目录
    loan_dir = FileUtil.path_join(
        current_app.config.get('LOAN_DIR'),
        loan_type.loan_dir,
        flow_type.flow_dir,
        loan_file.id
    )

    # 信息入库
    handle_info = loan_file.dao_add_info(loan_dir)
    return render_info(MyResponse(msg='接收资料成功', handle_info=handle_info))


@loan_bp.route('/loan_file/<string:id>', methods=[Method.GET.value])
@validated(LoanFileSchema, only=('id', ), locations=(Locations.VIEW_ARGS.value, ))
def get_loan(loan_file, id):
    """
    根据 ID 流水号查询贷款资料
    :param loan_file:
    :param id:
    :return:
    """
    # 查询贷款流水
    loan_file = LoanFileModel.query.get(loan_file.id)  # type: LoanFileModel
    Assert.is_true(is_not_empty(loan_file), '查无此数据', 200)
    loan_schema = LoanFileSchema().dump(loan_file)

    # 查询贷款主文件
    file = FileModel.query.get(loan_file.file_id)
    file_schema = FileSchema().dump(file)
    return render_info(MyResponse(
        msg='查询成功',
        loan_detail=loan_schema.data,
        loan_file=file_schema.data
    ))


@loan_bp.route('/loan_Type', methods=[Method.POST.value])
@validated(LoanTypeSchema, only=LoanTypeSchema().only_create(), consumes=ContentType.JSON.value)
def add_loan_type(loan_type):
    """
    添加贷款文件类型
    :type loan_type: LoanTypeModel
    :param loan_type: 
    :return: 
    """
    loan_type.dao_add()
    return render_info(MyResponse(msg='添加成功'))


@loan_bp.route('/flow_Type', methods=[Method.POST.value])
@validated(FlowTypeSchema, only=FlowTypeSchema().only_create(), consumes=ContentType.JSON.value)
def add_flow_type(flow_type):
    """
    添加流程类型
    :type flow_type: FlowTypeModel
    :param flow_type:
    :return:
    """
    flow_type.dao_add()
    return render_info(MyResponse(msg='添加成功'))


@loan_bp.route('/img_Type', methods=[Method.POST.value])
@validated(ImgTypeSchema, only=ImgTypeSchema().only_create(), consumes=ContentType.JSON.value)
def add_img_type(img_type):
    """
    添加图片类型
    :type img_type: ImgTypeModel
    :param img_type: 
    :return: 
    """
    img_type.dao_add()
    return render_info(MyResponse(code=0, msg='添加成功'))


@loan_bp.route('/push_info', methods=[Method.POST.value])
def push_info():
    print(json.dumps(request.json, indent=4, ensure_ascii=False))
    return render_info(MyResponse(msg='OK'))


if __name__ == '__main__':

    data = {
        'applicationNum': 'Ap125',
        'contractNum': 'Br125',
        'name': '张舟',
        'idCard': '341125199503200032',
        'agent': '东方裕隆',
        'title': '你大爷',
        'content': '氨基酸的哈哈去·',
        'loanType': {
            'loanTypeName': 'H'
        },
        'flowType': {
            'flowTypeName': 'FO'
        },
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
        'remarks': '备注信息...........',
        'push_url': 'http://127.0.0.1:5000/loan/push_info'
    }

    # data = {
    #     'loanTypeName': 'H',
    #     'loanDir': '贷后资料'
    # }

    # data = {
    #     'flowTypeName': 'FO',
    #     'flowDir': '一阶',
    #     'remarks': '你大爷特'
    # }

    # data = {
    #     'typeCode': 'abc',
    #     'typeExplain': '测试',
    #     'isOcr': '0',
    #     'remarks': '你大爷'
    # }

    # url = 'http://127.0.0.1:8088/loan/get_loan/2dc64710552b11e9acf95800e36a34d8'
    # res = requests.get(url=url, headers=json_headers)

    # url = 'http://127.0.0.1:8088/loan/loan_file'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:8088/loan/img_Type'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    #****************************************************************

    url = 'http://127.0.0.1:5000/loan/loan_file'
    res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:5000/loan/loan_file/7358d63a590311e9affa5800e36a34d8'
    # res = requests.get(url=url, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:5000/loan/loan_Type'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:5000/loan/flow_Type'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    # url = 'http://127.0.0.1:5000/loan/img_Type'
    # res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    print(res)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))


