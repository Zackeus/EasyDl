#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : ocr_api.py 
# @Software: PyCharm
# @Time : 2019/8/26 16:50

from flask import Blueprint, current_app

from models import OcrFileSchema, Mvsi, MvsiSchema, FileModel, SysData
from utils import Method, render_info, MyResponse, is_empty, is_not_empty, Assert, ContentType, validated, \
    codes, encodes
from utils.file import img
from utils.huawei_cloud import OCR, MvsiResultSchema
from utils.sys import get_app_sys, system

ocr_api_bp = Blueprint('ocr_api', __name__)


@ocr_api_bp.route('/mvsi', methods=[Method.POST.value])
@validated(OcrFileSchema, only=OcrFileSchema().only_create(), consumes=ContentType.JSON.value)
def ocr(ocrFile):
    """
    机动车销售发票 OCR识别
    :return:
    """
    app_sys = get_app_sys(ocrFile.app_sys_code)
    Assert.is_true(is_not_empty(app_sys), '无效的应用系统：{0}'.format(ocrFile.app_sys_code), codes.unprocessable)
    # 通过外键添加
    ocrFile.app_sys_id = app_sys.id

    file_model = FileModel()
    file_model.dao_create()

    # 资料写入磁盘
    file_path = encodes.base64_to_file(
        ocrFile.file_data.file_base64,
        current_app.config.get('OCR_FILE_DIR'),
        file_model.id,
        ocrFile.file_data.file_format)

    # OCR识别
    token = SysData().dao_get_key(system.SysKey.HUAWEI_CLOUD_TOKEN.value).value
    mvsi_result = OCR(token=token)\
        .mvsi(image_bs64=img.ImgUtil.img_compress(path=file_path, threshold=10))
    Assert.is_true(is_empty(mvsi_result.error_code),
                   'OCR FAILED: 【{0}】【{1}】'.format(mvsi_result.error_code, mvsi_result.error_msg))
    mvsi_result_json, errors = MvsiResultSchema(only=MvsiResultSchema().only_success()).dump(mvsi_result)
    Assert.is_true(is_empty(errors), errors)

    # 信息入库
    mvsi = Mvsi(**mvsi_result_json)
    mvsi.dao_add(ocrFile, file_model, file_path)

    # json 序列化
    mvsi_json, errors = MvsiSchema().dump(mvsi)
    Assert.is_true(is_empty(errors), errors)
    return render_info(MyResponse('OCR SUCCESS', results=mvsi_json))


if __name__ == '__main__':
    import json
    import requests
    from utils import ContentType

    # url = 'http://127.0.0.1:5000/api/ocr/mvsi'
    url = 'http://10.5.60.77:8088/api/ocr/mvsi'
    path = 'D:/AIData/11.jpg'

    data = {
        'appId': '1111',
        'fileData': {
            'fileName': 'text',
            'fileFormat': 'jpg',
            'fileBase64': img.ImgUtil.img_compress(path=path, threshold=10)
        },
        'appSysCode': 'OP_LOAN_H',
        'createBy': '17037',
        'remarks': '备注信息...........'
    }

    res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    print(res)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))

