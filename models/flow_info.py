#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : flow_info.py 
# @Software: PyCharm
# @Time : 2019/6/26 16:07


from models.basic import BaseSchema
from utils import BaseObject
from marshmallow import fields


class FlowInfo(BaseObject):

    def __init__(self, src, thumb, alt, pid, format=None):
        """
        流加载信息
        :param src: 文件地址
        :param thumb: 缩略地址
        :param alt: 简略信息
        :param format: 文件拓展
        :param pid: id流水
        """
        self.src = src
        self.thumb = thumb
        self.alt = alt
        self.pid = pid
        self.format = format


class FlowInfoSchema(BaseSchema):
    """
    流加载信息校验器
    """
    __model__ = FlowInfo

    src = fields.Str(required=True)
    thumb = fields.Str(required=True)
    alt = fields.Str(required=True)
    pid = fields.Str(required=True)
    format = fields.Str(required=True)
