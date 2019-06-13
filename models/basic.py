#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : basic.py 
# @Software: PyCharm
# @Time : 2019/3/26 8:46


from flask_login import current_user
from datetime import datetime
from marshmallow import fields, validate, Schema, post_load, post_dump

from extensions import db
from utils import IdGen, EncodingFormat, BaseObject, is_empty, is_not_empty


class BasicModel(BaseObject, db.Model):
    """
    模型基类
    """
    __abstract__ = True

    id = db.Column(db.String(length=64), name='ID', primary_key=True, default=IdGen.uuid(), comment='主键ID')
    create_by = db.Column(db.String(length=64), name='CREATE_BY', comment='创建者')
    update_by = db.Column(db.String(length=64), name='UPDATE_BY', comment='更新者')
    create_date = db.Column(db.DateTime, name='CREATE_DATE', default=datetime.utcnow, comment='创建日期')
    update_date = db.Column(db.DateTime, name='UPDATE_DATE', default=datetime.utcnow, comment='更新日期')
    remarks = db.Column(db.Text, name='REMARKS', comment='备注')

    def dao_create(self, id=None):
        self.id = id if id else IdGen.uuid()
        self.create_date = datetime.utcnow()
        self.update_date = datetime.utcnow()

        if is_empty(self.create_by):
            self.create_by = current_user.id if is_not_empty(current_user) else None
        self.update_by = self.create_by

    def dao_delete(self, subtransactions=False, nested=False):
        with db.auto_commit_db(subtransactions=subtransactions, nested=nested) as s:
            s.delete(self)

    def dao_get(self, id):
        return self.query.get(id)

    def dao_update(self, subtransactions=False, nested=False):
        with db.auto_commit_db(subtransactions=subtransactions, nested=nested) as s:
            if is_not_empty(current_user) and is_not_empty(current_user.id):
                self.update_by = current_user.id
            self.update_date = datetime.utcnow()
            # 将对象添加到session中，解决从缓存读取更新报 not in session 异常
            s.merge(self)


# noinspection PyMethodMayBeStatic
class BaseSchema(Schema):
    """
    校验器基类
    """
    __model__ = None

    id = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    create_by = fields.Str(validate=validate.Length(max=64), load_from='createBy')
    update_by = fields.Str(validate=validate.Length(max=64), load_from='updateBy')
    create_date = fields.DateTime()
    update_date = fields.DateTime()
    remarks = fields.Str()

    @post_load
    def make_object(self, data):
        """
        序列化对象
        :param data:
        :return:
        """
        return self.__model__(**data) if self.__model__ else data

    @post_dump
    def make_dict(self, data):
        """
        序列化字典
        :type data: dict
        :param data:
        :return:
        """
        new_data = {}
        for key, value in data.items():
            key = EncodingFormat.pep8_to_hump(key)
            new_data[key] = value
        return new_data

    def only_create(self):
        return 'create_by', 'remarks',

    def only_delete(self):
        return 'id',

    def only_get(self):
        return 'id',

    def only_put(self):
        return 'id', 'update_by', 'remarks'

    def only_update(self):
        return 'update_by',

    def only_page(self):
        return '',


class DataEntity(BaseObject):

    def __init__(self, id, current_user, del_flag='0', is_new_record=False, remarks=None,
                 create_by=None, update_by=None, create_date=datetime.utcnow(), update_date=None):
        """

        :param id: 实体编号（唯一标识）
        :param current_user: 当前用户
        :param del_flag: 删除标记（0：正常；1：删除；2：审核）
        :param is_new_record: 是否是新记录（默认：false）
        :type id: str
        :type is_new_record: bool
        """
        self.id = id
        self.current_user = current_user
        self.create_by = create_by
        self.update_by = update_by
        self.create_date = create_date
        self.update_date = update_date if update_date else datetime.utcnow()
        self.remarks = remarks

        self.del_flag = del_flag
        self.is_new_record = is_new_record

    def dao_create(self, id=None):
        pass

    def dao_delete(self):
        pass

    def dao_get(self, id):
        pass

    def dao_update(self):
        pass


class DataEntitySchema(Schema):
    """
    校验器基类
    """
    __model__ = None

    id = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    create_date = fields.DateTime(load_from='createDate')
    update_date = fields.DateTime(load_from='updateDate')
    remarks = fields.Str(validate=validate.Length(max=255))

    del_flag = fields.Str(required=True, validate=validate.Length(min=1, max=1), default='0', load_from='delFlag')
    is_new_record = fields.Boolean(load_from='isNewRecord')

    current_user = fields.Nested(
        'UserSchema',
        only=('id', 'login_name', 'password', 'no', 'name', 'phone', 'mobile'),
        exclude=('current_user', 'new_password', ),
        load_from='currentUser'
    )

    @post_load
    def make_object(self, data):
        """
        序列化对象
        :param data:
        :return:
        """
        return self.__model__(**data) if self.__model__ else data

    @post_dump
    def make_dict(self, data):
        """
        序列化字典
        :type data: dict
        :param data:
        :return:
        """
        new_data = {}
        for key, value in data.items():
            key = EncodingFormat.pep8_to_hump(key)
            new_data[key] = value
        return new_data

    def only_create(self):
        pass

    # noinspection PyMethodMayBeStatic
    def only_delete(self):
        return 'id',

    # noinspection PyMethodMayBeStatic
    def only_get(self):
        return 'id',

    def only_update(self):
        pass

    def partial_db(self):
        """
        db查询过滤字段
        :return:
        """
        pass









