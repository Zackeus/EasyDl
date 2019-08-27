#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : sys.py 
# @Software: PyCharm
# @Time : 2019/8/27 16:09

from extensions import scheduler

from models import SysData

from utils.sys import system
from utils.huawei_cloud import OCR


def huawei_cloud_token():
    """
    华为云鉴权信息更新
    :return:
    """
    with scheduler.app.app_context():
        sys_data = SysData().dao_get_key(system.SysKey.HUAWEI_CLOUD_TOKEN.value)
        huawei_ocr = OCR()
        sys_data.value = huawei_ocr.token
        sys_data.dao_update()

