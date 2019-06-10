#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 系统菜单
# @Author : Zackeus
# @File : menu.py 
# @Software: PyCharm
# @Time : 2019/6/6 10:27


from extensions import db, cache
from models.basic import BasicModel, BaseSchema

from utils import validates, Unicode, Assert, is_not_empty, is_empty, codes
from marshmallow import fields


class Menu(BasicModel):
    """
    系统菜单
    """
    __tablename__ = 'SYS_MENU'

    parent_id = db.Column(
        db.String(length=64),
        db.ForeignKey('SYS_MENU.ID'),
        name='PARENT_ID',
        index=True,
        comment='父级菜单ID'
    )
    name = db.Column(db.String(length=30), name='NAME', nullable=False, comment='菜单名称')
    icon = db.Column(db.String(length=64), name='ICON', comment='菜单图标')
    sort = db.Column(db.Integer, name='SORT', default=1, comment='排序')
    href = db.Column(db.Text, name='HREF', comment='链接')
    spread = db.Column(db.Boolean, name='SPREAD', nullable=False, default=False, comment='是否展开')

    menu = db.relationship(
        argument='Menu',
        back_populates='children',
        remote_side='Menu.id'
    )

    children = db.relationship(
        argument='Menu',
        back_populates='menu',
        cascade='all'
    )

    @cache.memoize()
    def dao_get_all_tree_menus(self):
        """
        获取全部一级菜单
        :return:
        """
        return self.query.filter(Menu.parent_id == '1').order_by(Menu.sort.asc()).all()

    @cache.memoize()
    def dao_get_all_menus(self, id, is_dump=False):
        """
        获取全部左侧菜单树
        :param id:
        :param is_dump: 是否序列化字典(序列化尽量写在同一个方法，因为relationship的懒加载机制，结合缓存会报Session异常)
        :return:
        """
        menus = self.query.filter(Menu.parent_id == id).order_by(Menu.sort.asc()).all()

        if is_dump:
            Assert.is_true(is_not_empty(menus), '查无此数据', codes.no_data)

            menus, errors = MenuSchema().dump(menus, many=True)
            Assert.is_true(is_empty(errors), errors)
        return menus

    def dao_add(self, **kwargs):
        """
        添加菜单
        :param kwargs:
        :return:
        """
        super().dao_create()
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)


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
        validate=validates.MyLength(max=64, encode_str=Unicode.UTF_8.value),
    )
    sort = fields.Integer()
    href = fields.Str()
    spread = fields.Boolean(required=True)

    children = fields.Nested('self', dump_only=True, many=True)

    def only_create(self):
        return super().only_create() + ('parent_id', 'name', 'icon', 'sort', 'href', 'spread')
