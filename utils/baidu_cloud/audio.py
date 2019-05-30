#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : audio.py 
# @Software: PyCharm
# @Time : 2019/5/15 9:00


import requests
import json
from marshmallow import Schema, fields, post_load

import encodes
from utils.errors import MyError
from utils.request import codes, ContentType
from utils.object_util import is_not_empty, BaseObject
from utils.baidu_cloud.baidu import BaiduCloud
from utils.decorators import auto_wired
from utils.file.file import FileFormat


class Audio(BaseObject):

    @auto_wired('utils.baidu_cloud.audio.Audio')
    def __init__(self, app_id=None, api_key=None, secret_key=None, baidu_cloud=None, **kwargs):
        """
        音频应用
        :param app_id:
        :param api_key:
        :param secret_key:
        :param baidu_cloud:
        """
        self.app_id = app_id
        self.token = None
        if is_not_empty(api_key) and is_not_empty(secret_key):
            baidu_cloud = BaiduCloud(api_key, secret_key)
            baidu_cloud.init_token()
        elif is_not_empty(baidu_cloud) and is_not_empty(baidu_cloud.token):
            pass
        else:
            raise MyError('缺失鉴权 Token 参数.')
        self.token = baidu_cloud.token

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def offline_transfer(self, call_id, url=None, company_name=None, agent_file_url=None,
                         call_back_url=None, suffix=FileFormat.PCM.value):
        """
        音频文件离线转写
        :param url: 转写接口
        :param str call_id: 唯一电话识别参数,建议使用UUID,不超过128位,业务方保证(appId,callId)联合唯一
        :param str company_name: 录音所属公司
        :param str agent_file_url: 用户销售侧文件存储URL或者单个文件的混音文件
        :param str call_back_url: 用户获取翻译结果回调接口,若填写则通过地址回调，若不填则须客户使用查询结果接口进行查询
        :param str suffix: 文件名后缀
        :return:
        """
        url = url if url else getattr(self, 'offline_transfer_url', None)
        url = url.format(access_token=self.token)

        company_name = company_name if company_name else getattr(self, 'company_name', None)
        call_back_url = call_back_url if call_back_url else getattr(self, 'call_back_url', None)

        agent_file_url = agent_file_url if agent_file_url else getattr(self, 'agent_file_url', None)
        agent_file_url = agent_file_url.format(call_id=call_id)

        transfer_params = dict(
            appId=self.app_id,
            companyName=company_name,
            callId=call_id,
            agentFileUrl=agent_file_url,
            callbackUrl=call_back_url,
            suffix=suffix.lower()
        )

        res = requests.post(url=url, data=json.dumps(transfer_params), headers=ContentType.JSON_UTF8.value)
        res.encoding = encodes.Unicode.UTF_8.value
        print(res.status_code)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))
        return json.dumps(res.json(), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    audio = Audio(api_key='vNkk0VNG8jexKvIKBHyQkKd1', secret_key='PYG0w3zo0wka99NcKxkDS7IMwpTtSr2b')
    url = 'https://aip.baidubce.com/rpc/2.0/search/info?access_token={access_token}'
    url = url.format(access_token=audio.token)

    params = {
        'category': 'OFFLINE_ASR_RESULT',
        'paras': {
            'appId': 16217202,
            'callId': '84e6777676c011e9a51a5800e36a34d8'
        }
    }

    res = requests.post(url=url, data=json.dumps(params), headers=ContentType.JSON_UTF8.value)
    res.encoding = encodes.Unicode.UTF_8.value
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    with open('D:/AIData/8k.txt', 'a') as f:
        for info in json.loads(res.json().get('data').get('content')):
            print(info)
            f.writelines(str(info) + '\n')

