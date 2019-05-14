#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 信息工具类
# @Author : Zackeus
# @File : msg.py 
# @Software: PyCharm
# @Time : 2019/4/3 14:34


import requests
from marshmallow import Schema, fields, validate

from utils.request import ContentType
from utils.encodes import Unicode
from utils.errors import MyError
from utils.decorators import auto_wired


class WXMsg(object):

    __PREFIX = '【裕隆汽车金融】'

    @auto_wired('utils.msg.WXMsg')
    def __init__(self, url, request_sys,  msg_content, agent_id, receiver_party_id, receiver_user_id,
                 request_user='', receiver_name='', receiver_company='裕隆汽车金融(中国)有限公司',
                 receiver_role='', send_datetime='', repeat_times=1, repeat_interval=60, application_number='',
                 external_contract_nbr=''):
        """
        微信信息实体
        :param url:微信发送地址
        :param request_sys:来源系统
        :param msg_content:短信内容(必填)
        :param agent_id:应用ID（必填）
        :param receiver_party_id:组ID（必填）
        :param receiver_user_id:员工ID（必填）
        :param request_user:来源用户
        :param receiver_name:接收人
        :param receiver_company:接收人公司
        :param receiver_role:接收人角色
        :param send_datetime:发送日期时间（为null为立即发送）
        :param repeat_times:重送次数（默认为1）
        :param repeat_interval:重送间隔(默认为60分钟)
        :param application_number:申请号
        :param external_contract_nbr:合同号
        """
        self.url = url
        self.request_sys = request_sys
        self.msg_content = msg_content if str(msg_content).startswith(self.__PREFIX) else \
            self.__PREFIX + str(msg_content)
        self.agent_id = agent_id
        self.receiver_party_id = receiver_party_id
        self.receiver_user_id = receiver_user_id
        self.request_user = request_user
        self.receiver_name = receiver_name
        self.receiver_company = receiver_company
        self.receiver_role = receiver_role
        self.send_datetime = send_datetime
        self.repeat_times = repeat_times
        self.repeat_interval = repeat_interval
        self.application_number = application_number
        self.external_contract_nbr = external_contract_nbr

    def send_wx(self):
        """
        发送微信信息
        :return:
        """
        res = requests.post(
            url=self.url,
            json=WXMsgSchema().dump(self).data,
            headers=ContentType.JSON_UTF8.value
        )
        res.encoding = Unicode.UTF_8.value
        if res is None or res.status_code != requests.codes.ok:
            raise MyError(code=requests.codes.server_error,
                          msg='发送微信信息请求失败：{0}'.format(str(res.status_code)
                                                      if res is not None else requests.codes.bad))
        return res.json()


class WXMsgSchema(Schema):

    request_sys = fields.Str(required=True, validate=validate.Length(min=1), dump_to='Request_sys')
    msg_content = fields.Str(required=True, validate=validate.Length(min=1), dump_to='Msg_content')
    agent_id = fields.Str(required=True, validate=validate.Length(min=1), dump_to='Agentid')
    receiver_party_id = fields.Str(required=True, validate=validate.Length(min=1), dump_to='Receiver_partyid')
    receiver_user_id = fields.Str(required=True, validate=validate.Length(min=1), dump_to='Receiver_userid')
    request_user = fields.Str(dump_to='Request_user')
    receiver_name = fields.Str(dump_to='Receiver_name')
    receiver_company = fields.Str(dump_to='Receiver_company')
    receiver_role = fields.Str(dump_to='Receiver_role')
    send_datetime = fields.Str(dump_to='Send_datetime')
    repeat_times = fields.Integer(dump_to='Repeat_times', missing=1)
    repeat_interval = fields.Integer(dump_to='Repeat_interval', missing=60)
    application_number = fields.Str(dump_to='Application_number')
    external_contract_nbr = fields.Str(dump_to='External_contract_nbr')


if __name__ == '__main__':
    # print(WXMsg(
    #     request_sys='Error',
    #     msg_content='【裕隆汽车金融】测试',
    #     agent_id='1000029',
    #     receiver_party_id='',
    #     receiver_user_id='ZhangZhou',
    #     request_user='zhangzhou',
    #     receiver_name='张舟'
    # ).send_wx())

    pass
