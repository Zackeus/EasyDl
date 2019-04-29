#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : loan_util.py 
# @Software: PyCharm
# @Time : 2019/4/24 16:48


import os
from datetime import datetime

from models.loan.loan_file import LoanFileModel
from models.loan.loan_type import LoanTypeModel
from models.loan.flow_type import FlowTypeModel


def creat_dir(base_dir, loan_file, loan_type, flow_type):
    """
    创建贷款资料目录
    :param base_dir: 基目录
    :param LoanFileModel loan_file: 贷款模型
    :param LoanTypeModel loan_type: 贷款类型
    :param FlowTypeModel flow_type: 流程类型
    :return:
    """
    __hours = [15, 17]
    __format = '{month}月{day}日{hour}点之{label}'
    format = None
    i = datetime.now()
    for hour in __hours:
        if i.hour < hour:
            format = format if format else __format.format(month=i.month, day=i.day, hour=hour, label='前')
            break
        else:
            format = __format.format(month=i.month, day=i.day, hour=hour, label='后')
    loan_dir = os.path.join(
        base_dir,
        loan_type.loan_dir,
        flow_type.flow_dir,
        format,
        loan_file.name + loan_file.id_card + loan_type.loan_type_name + '-' + loan_file.id
    )
    return loan_dir

