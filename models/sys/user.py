#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : user.py 
# @Software: PyCharm
# @Time : 2019/4/16 11:07


from flask_login import UserMixin
from datetime import datetime
from flask import current_app
from marshmallow import fields, validate

from utils.decorators import result_mapper
from extensions import db, cache
from models.basic import DataEntity, DataEntitySchema
from utils import validates as MyValidates


class User(DataEntity, UserMixin):

    def __init__(self, id=None, current_user=None, company=None, office=None, login_name=None,
                 password=None, no=None, name=None, email=None, phone=None, mobile=None,
                 user_type=None, login_ip=None, login_date=None, login_flag=None, photo=None,
                 old_login_name=None, new_password=None, old_login_ip=None, old_login_date=None,
                 role=None, role_list=None, **kwargs):
        """

        :arg str id:
        :param current_user:
        :param company: 归属公司
        :param office: 归属部门
        :arg str login_name: 登录名
        :arg str password: 密码
        :arg str no: 工号
        :arg str name: 姓名
        :arg str email: 邮箱
        :arg str phone: 电话
        :arg str mobile: 手机
        :arg str user_type: 用户类型
        :arg str login_ip: 最后登陆IP
        :arg datetime login_date: 最后登陆日期
        :arg str login_flag: 是否允许登陆
        :arg str photo: 头像
        :arg str old_login_name: 原登录名
        :arg str new_password: 新密码
        :arg str old_login_ip: 上次登陆IP
        :arg datetime old_login_date: 上次登陆日期
        :param role: 角色
        :param role_list: 角色列表
        """
        super(User, self).__init__(id, current_user, **kwargs)
        self.company = company
        self.office = office
        self.login_name = login_name
        self.password = password
        self.no = no
        self.name = name
        self.email = email
        self.phone = phone
        self.mobile = mobile
        self.user_type = user_type
        self.login_ip = login_ip
        self.login_date = login_date
        self.login_flag = login_flag
        self.photo = photo
        self.old_login_name = old_login_name
        self.new_password = new_password
        self.old_login_ip = old_login_ip
        self.old_login_date = old_login_date
        self.role = role
        self.role_list = role_list

    def validate_password(self, plain_password):
        """
        验证密码
        :param plain_password: 明文密码
        :return:
        """
        from utils import sys
        return sys.validate_password(plain_password, self.password)

    @cache.memoize(timeout=60 * 60 * 2)
    @result_mapper(module_name='models.sys.user', schema_cls='UserSchema')
    def dao_get(self, id):
        sql = "SELECT a.id, a.id AS 'current_user.id', a.company_id AS 'company.id', a.office_id AS 'office.id', " \
              "a.login_name, a.login_name AS 'current_user.login_name', a.password, " \
              "a.password AS 'current_user.password', a.no, a.no AS 'current_user.no', " \
              "a.name, a.name AS 'current_user.name', " \
              "a.email, a.phone, a.phone AS 'current_user.phone', " \
              "a.mobile, a.mobile AS 'current_user.mobile', a.user_type, a.login_ip, a.login_date, " \
              "a.remarks, a.login_flag, a.photo, a.create_by AS 'create_by.id', a.create_date, " \
              "a.update_by AS 'update_by.id', a.update_date, a.del_flag, c.name AS 'company.name', " \
              "c.parent_id AS 'company.parent.id', c.parent_ids AS 'company.parent_ids', " \
              "ca.id AS 'company.area.id', ca.name AS 'company.area.name', " \
              "ca.parent_id AS 'company.area.parent.id', ca.parent_ids AS 'company.area.parent_ids', " \
              "o.name AS 'office.name', o.parent_id AS 'office.parent.id', o.parent_ids AS 'office.parent_ids', " \
              "oa.id AS 'office.area.id', oa.name AS 'office.area.name', " \
              "oa.parent_id AS 'office.area.parent.id', oa.parent_ids AS 'office.area.parent_ids', " \
              "cu.id AS 'company.primary_person.id', cu.name AS 'company.primary_person.name', " \
              "cu2.id AS 'company.deputy_person.id', cu2.name AS 'company.deputy_person.name', " \
              "ou.id AS 'office.primary_person.id', ou.name AS 'office.primary_person.name', " \
              "ou2.id AS 'office.deputy_person.id', ou2.name AS 'office.deputy_person.name'" \
              "FROM [jeesite-yfc].[dbo].[sys_user] a " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_office] c ON c.id = a.company_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_area] ca ON ca.id = c.area_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_office] o ON o.id = a.office_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_area] oa ON oa.id = o.area_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] cu ON cu.id = c.primary_person " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] cu2 ON cu2.id = c.deputy_person " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] ou ON ou.id = o.primary_person " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] ou2 ON ou2.id = o.deputy_person " \
              "WHERE a.id = :id AND a.del_flag = :del_flag "
        with db.auto_commit_db() as s:
            res = s.execute(sql,
                            params={'id': id, 'del_flag': self.del_flag},
                            bind=db.get_engine(current_app, bind='JEESITE-YFC'))
            return res._metadata.keys, res.cursor.fetchone()

    @result_mapper(module_name='models.sys.user', schema_cls='UserSchema')
    def dao_get_by_login_name(self, login_name):
        sql = "SELECT a.id, a.id AS 'current_user.id', a.company_id AS 'company.id', a.office_id AS 'office.id', " \
              "a.login_name, a.login_name AS 'current_user.login_name', a.password, " \
              "a.password AS 'current_user.password', a.no, a.no AS 'current_user.no', " \
              "a.name, a.name AS 'current_user.name', " \
              "a.email, a.phone, a.phone AS 'current_user.phone', " \
              "a.mobile, a.mobile AS 'current_user.mobile', a.user_type, a.login_ip, a.login_date, " \
              "a.remarks, a.login_flag, a.photo, a.create_by AS 'create_by.id', a.create_date, " \
              "a.update_by AS 'update_by.id', a.update_date, a.del_flag, c.name AS 'company.name', " \
              "c.parent_id AS 'company.parent.id', c.parent_ids AS 'company.parent_ids', " \
              "ca.id AS 'company.area.id', ca.name AS 'company.area.name', " \
              "ca.parent_id AS 'company.area.parent.id', ca.parent_ids AS 'company.area.parent_ids', " \
              "o.name AS 'office.name', o.parent_id AS 'office.parent.id', o.parent_ids AS 'office.parent_ids', " \
              "oa.id AS 'office.area.id', oa.name AS 'office.area.name', " \
              "oa.parent_id AS 'office.area.parent.id', oa.parent_ids AS 'office.area.parent_ids', " \
              "cu.id AS 'company.primary_person.id', cu.name AS 'company.primary_person.name', " \
              "cu2.id AS 'company.deputy_person.id', cu2.name AS 'company.deputy_person.name', " \
              "ou.id AS 'office.primary_person.id', ou.name AS 'office.primary_person.name', " \
              "ou2.id AS 'office.deputy_person.id', ou2.name AS 'office.deputy_person.name'" \
              "FROM [jeesite-yfc].[dbo].[sys_user] a " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_office] c ON c.id = a.company_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_area] ca ON ca.id = c.area_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_office] o ON o.id = a.office_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_area] oa ON oa.id = o.area_id " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] cu ON cu.id = c.primary_person " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] cu2 ON cu2.id = c.deputy_person " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] ou ON ou.id = o.primary_person " \
              "LEFT JOIN [jeesite-yfc].[dbo].[sys_user] ou2 ON ou2.id = o.deputy_person " \
              "WHERE a.login_name = :login_name AND a.del_flag = :del_flag "
        with db.auto_commit_db() as s:
            res = s.execute(sql,
                            params={'login_name': login_name, 'del_flag': self.del_flag},
                            bind=db.get_engine(current_app, bind='JEESITE-YFC'))
            return res._metadata.keys, res.cursor.fetchone()


class UserSchema(DataEntitySchema):
    """
    用户校验器
    """
    __model__ = User

    login_name = fields.Str(required=True,
                            validate=MyValidates.MyLength(min=1, max=100, not_empty=False),
                            load_from='loginName')

    password = fields.Str(required=True, validate=MyValidates.MyLength(min=1, max=100, not_empty=False))
    no = fields.Str(validate=validate.Length(max=100))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Str(validate=validate.Length(max=200))
    phone = fields.Str(validate=validate.Length(max=200))
    mobile = fields.Str(validate=validate.Length(max=200))
    user_type = fields.Str(validate=validate.Length(max=1), load_from='userType')
    login_ip = fields.Str(validate=validate.Length(max=100), load_from='loginIp')
    login_date = fields.DateTime(load_from='loginDate')
    login_flag = fields.Str(validate=validate.Length(max=64), load_from='loginFlag')
    photo = fields.Str(validate=validate.Length(max=1000))
    old_login_name = fields.Str(validate=validate.Length(min=1, max=100), load_from='oldLoginName')
    new_password = fields.Str(required=True, validate=validate.Length(min=1, max=100), load_from='newPassword')
    old_login_ip = fields.Str(load_from='oldLoginIp')
    old_login_date = fields.DateTime(load_from='oldLoginDate')

    # file_data = fields.Nested(
    #     FileSchema,
    #     required=True,
    #     load_only=True,
    #     load_from='fileData'
    # )
    #
    # loan_type = fields.Nested(
    #     LoanTypeSchema,
    #     only=('id', 'loan_type_name', 'loan_dir'),
    #     required=True,
    #     load_from='loanType'
    # )

    def partial_db(self):
        return 'new_password',

    # noinspection PyMethodMayBeStatic
    def only_login(self):
        return 'login_name', 'password'













