#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : page.py 
# @Software: PyCharm
# @Time : 2019/6/12 17:06


from marshmallow import fields

from extensions import db
from models.basic import BasicModel, BaseSchema
from utils import validates, Unicode, codes


class Page(BasicModel):

    __abstract__ = True

    code = db.Column(db.String(length=64), name='CODE', comment='数据状态的字段名称 成功默认为0')
    msg = db.Column(db.Text, name='MSG', comment='状态信息的字段名称')
    page = db.Column(db.Integer, name='PAGE', comment='当前页码')
    page_size = db.Column(db.Integer, name='PAGE_SIZE', comment='每页限制条数')
    total = db.Column(db.Integer, name='TOTAL', comment='总条数')
    total_page = db.Column(db.Integer, name='TOTAL_PAGE', comment='总页数')
    data = db.Column(db.Text, name='DATA', comment='分页数据')

    def init_pagination(self, pagination, msg='查询成功.'):
        """
        根据 pagination 实例化分页对象
        :param pagination:
        :param msg:
        :return:
        """
        self.code = codes.success
        self.msg = msg
        self.page = pagination.page
        self.page_size = pagination.per_page
        self.total = pagination.total
        self.total_page = pagination.pages
        self.data = pagination.items


class PageSchema(BaseSchema):
    """
    分页实体校验器
    """
    __model__ = Page

    code = fields.Str(validate=validates.MyLength(max=64, encode_str=Unicode.UTF_8.value))
    msg = fields.Str()
    page = fields.Integer(required=True)
    page_size = fields.Integer(required=True, load_from='pageSize')
    total = fields.Integer()
    total_page = fields.Integer(load_from='totalPage')
    data = fields.Str(dump_only=True)

    def only_create(self):
        return super().only_create() + ('page', 'page_size')
