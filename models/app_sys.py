#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : sys_code.py 
# @Software: PyCharm
# @Time : 2019/5/23 13:57


from marshmallow import fields

from extensions import db, cache
from models.basic import BasicModel, BaseSchema
from utils import validates


class AppSys(BasicModel):
    """
    应用系统
    """
    __tablename__ = 'APP_SYS'

    code = db.Column(
        db.String(length=64),
        name='CODE',
        index=True,
        unique=True,
        nullable=False,
        comment='系统代号'
    )

    desc = db.Column(db.String(length=50), name='DESC', nullable=False, comment='代号描述')

    def dao_add(self, **kwargs):
        super().dao_create()
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)

    @cache.memoize()
    def dao_get(self, id):
        """
        根据id查询数据
        :param id:
        :return:
        """
        return super().dao_get(id)

    @cache.memoize()
    def dao_get_by_code(self, code):
        """
        根据代号字符查询
        :param str code:
        :return:
        """
        return self.query.filter_by(code=code).first()


class AppSysSchema(BaseSchema):
    """
    应用系统校验器
    """
    __model__ = AppSys

    code = fields.Str(required=True, validate=validates.MyLength(min=1, max=64, not_empty=False))
    desc = fields.Str(required=True, validate=validates.MyLength(min=1, max=50, not_empty=False))

    def only_create(self):
        return super().only_create() + ('code', 'desc')
