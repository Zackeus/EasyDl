#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 系统字典
# @Author : Zackeus
# @File : sys_dict.py 
# @Software: PyCharm
# @Time : 2019/6/12 14:40


from marshmallow import fields

from extensions import db, cache
from models.basic import BasicModel, BaseSchema
from utils import validates, Unicode


class SysDict(BasicModel):
    """
    系统字典
    """
    __tablename__ = 'SYS_DICT'

    __table_args__ = (
        db.UniqueConstraint('VALUE', 'TYPE', name='uix_SYS_DICT_VALUE_TYPE'),
    )

    value = db.Column(db.String(length=64), name='VALUE', index=True, comment='数据值')
    label = db.Column(db.String(length=64), name='LABEL', nullable=False, comment='标签名')
    type = db.Column(db.String(length=64), name='TYPE', index=True, nullable=False, comment='类型')
    description = db.Column(db.String(length=225), name='DESCRIPTION', comment='描述')
    sort = db.Column(db.Integer, name='SORT', default=10, comment='排序')

    @cache.memoize()
    def dao_get_all(self):
        """
        获取全部字典
        :return:
        """
        dicts = self.query.order_by(SysDict.sort.asc()).all()
        return dicts

    @cache.memoize()
    def dao_get_types(self):
        """
        查询字典类型列表
        :return:
        """
        types = []
        for dict_type in self.query.with_entities(SysDict.type).distinct().all():
            types.append(dict_type[0])
        return types


class SysDictSchema(BaseSchema):
    """
    系统字典校验器
    """
    __model__ = SysDict

    value = fields.Str(validate=validates.MyLength(max=64, encode_str=Unicode.UTF_8.value))
    label = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=64, encode_str=Unicode.UTF_8.value, not_empty=False)
    )
    type = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=64, encode_str=Unicode.UTF_8.value, not_empty=False)
    )
    description = fields.Str(validate=validates.MyLength(max=225, encode_str=Unicode.UTF_8.value))
    sort = fields.Integer()

    def only_create(self):
        return super().only_create() + ('value', 'label', 'type', 'description', 'sort')

    def only_page(self):
        return {
            'type': fields.Str()
        }
