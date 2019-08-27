#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : sys_data.py 
# @Software: PyCharm
# @Time : 2019/8/27 15:28


from extensions import db, cache
from models.basic import BasicModel


class SysData(BasicModel):
    """
    系统数据
    """
    __tablename__ = 'SYS_DATA'

    key = db.Column(db.String(length=64), name='KEY', index=True, nullable=False, unique=True, comment='数据键值')
    value = db.Column(db.Text, name='VALUE', comment='数据值')
    description = db.Column(db.String(length=225), name='DESCRIPTION', comment='描述')

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    @cache.memoize()
    def dao_get(self, id):
        """

        :param id:
        :return:
        """
        return super().dao_get(id)

    @cache.memoize()
    def dao_get_key(self, key):
        """
        根据键值查询数据
        :param key:
        :return:
        """
        return self.query.filter(SysData.key == key).first()

    @cache.delete_cache([dao_get, dao_get_key])
    def dao_add(self, **kwargs):
        """
        更新数据
        :param kwargs:
        :return:
        """
        super().dao_create()
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)

    @cache.delete_cache([dao_get, dao_get_key])
    def dao_update(self, **kwargs):
        """
        更新数据
        :param kwargs:
        :return:
        """
        super().dao_update(**kwargs)