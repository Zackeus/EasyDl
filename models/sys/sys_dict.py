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
from utils import validates, Unicode, is_not_empty, is_empty, Assert


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

    def dao_find_page(self, page, error_out=False):
        """
        分页条件查询
        :param page:
        :param error_out:
        :return:
        """
        # 条件查询
        filter = []

        if is_not_empty(self.type):
            filter.append(SysDict.type == self.type)
        if is_not_empty(self.description):
            filter.append(SysDict.description.like('%{description}%'.format(description=self.description)))

        pagination = self.query.filter(*filter).\
            order_by(SysDict.sort.asc(), SysDict.type.asc(), SysDict.create_date.asc()).\
            paginate(page=page.page, per_page=page.page_size, error_out=error_out)
        page.init_pagination(pagination)

        # 数据序列化 json
        data_dict, errors = SysDictSchema().dump(page.data, many=True)
        Assert.is_true(is_empty(errors), errors)
        page.data = data_dict
        return page, pagination.query

    @cache.memoize()
    def dao_get(self, id):
        """

        :param id:
        :return:
        """
        return super().dao_get(id)

    @cache.memoize()
    def dao_get_type_value(self, type, value):
        """
        根据类型和value查询字典
        :param type:
        :param value:
        :return:
        """
        return self.query.filter(SysDict.type == type, SysDict.value == value).first()

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

    @cache.delete_cache([dao_get, dao_get_all, dao_get_types, dao_get_type_value])
    def dao_add(self, **kwargs):
        """
        添加字典
        :param kwargs:
        :return:
        """
        super().dao_create()
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)

    @cache.delete_cache([dao_get, dao_get_all, dao_get_types, dao_get_type_value])
    def dao_delete(self, **kwargs):
        """
        删除字典
        :param kwargs:
        :return:
        """
        super().dao_delete(**kwargs)


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
        return super().only_page() + ('type', 'description')
