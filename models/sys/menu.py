#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 系统菜单
# @Author : Zackeus
# @File : menu.py 
# @Software: PyCharm
# @Time : 2019/6/6 10:27


from extensions import db
from models.basic import BasicModel, BaseSchema

from utils import validates, Unicode
from marshmallow import fields


class Menu(BasicModel):
    """
    系统菜单
    """
    __tablename__ = 'SYS_MENU'

    parent_id = db.Column(db.String(length=64), name='PARENT_ID', index=True, comment='父级菜单ID')
    name = db.Column(db.String(length=30), name='NAME', nullable=False, comment='菜单名称')
    icon = db.Column(db.String(length=64), name='ICON', nullable=False, comment='菜单图标')
    sort = db.Column(db.Integer, name='SORT', default=1, comment='排序')
    href = db.Column(db.Text, name='HREF', comment='链接')
    spread = db.Column(db.Boolean, name='SPREAD', nullable=False, default=False, comment='是否展开')

    @property
    def children(self):
        """
        查询全部子级菜单
        :return:
        """
        return self.query.filter(Menu.parent_id == self.id).order_by(Menu.sort.asc()).all()


class MenuSchema(BaseSchema):
    """
    系统菜单校验器
    """
    __model__ = Menu

    parent_id = fields.Str(
        validate=validates.MyLength(min=1, max=64, not_empty=False, encode_str=Unicode.UTF_8.value),
        load_from='parentId'
    )
    name = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=30, not_empty=False, encode_str=Unicode.UTF_8.value),
    )
    icon = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=64, not_empty=False, encode_str=Unicode.UTF_8.value),
    )
    sort = fields.Integer()
    href = fields.Str()
    spread = fields.Boolean(required=True)
