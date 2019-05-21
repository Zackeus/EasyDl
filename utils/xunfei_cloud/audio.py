#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : audio.py 
# @Software: PyCharm
# @Time : 2019/5/15 16:08


import requests
import json

from utils import Unicode
from utils.xunfei_cloud.xunfei import Sign
# from utils.file.media import Audio
from utils.object_util import is_not_empty, BaseObject
from utils.decorators import auto_wired
from utils.errors import MyError


class Audio(BaseObject):

    @auto_wired('utils.xunfei_cloud.audio.Audio')
    def __init__(self, app_id=None, api_key=None, sign=None):
        """
        讯飞开放平台数字签名
        :param str app_id: 讯飞开放平台应用ID
        :param str api_key: 讯飞开放平台应用秘钥
        :param Sign sign: 讯飞开放平台数字签名对象

        """
        if is_not_empty(app_id) and is_not_empty(api_key):
            sign = Sign(app_id, api_key)
        elif is_not_empty(sign) and is_not_empty(sign.signa):
            pass
        else:
            raise MyError('缺失数字签名参数.')

        self.app_id = app_id
        self.ts = sign.ts
        self.base_string = sign.base_string
        self.signa = sign.signa

    def offline_transfer(self):
        """
        音频离线转写
        :return:
        """
        pass

    def _prepare(self):
        """
        预处理
        :return:
        """
        pass


class SliceIdGenerator:
    """slice id生成器"""

    def __init__(self):
        self.__ch = 'aaaaaaaaa`'

    def get_next_slice_id(self):
        ch = self.__ch
        j = len(ch) - 1
        while j >= 0:
            cj = ch[j]
            if cj != 'z':
                ch = ch[:j] + chr(ord(cj) + 1) + ch[j + 1:]
                break
            else:
                ch = ch[:j] + 'a' + ch[j + 1:]
                j = j - 1
        self.__ch = ch
        return self.__ch


def prepare(app_id, sign, ts, file_path, slice_num=1, has_seperate=True, speaker_number='2'):
    """
    预处理
    :param str app_id: 讯飞开放平台应用ID
    :param str sign: 加密数字签名（基于HMACSHA1算法)
    :param str ts: 当前时间戳，从1970年1月1日0点0分0秒开始到现在的秒数
    :param file_path: 文件路径
    :param slice_num: 文件分片数目（时长小于 5 min 音频，不建议分片，此时slice_num=1）
    :param has_seperate: 转写结果中是否包含发音人分离信息
    :param speaker_number: 发音人个数，可选值：0-10，0表示盲分
    :return:
    """
    has_seperate = 'true' if has_seperate else 'false'
    url = 'http://raasr.xfyun.cn/api/prepare'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': 'UTF-8'
    }

    audio_file = Audio.probe(file_path)
    params = dict(
        app_id=app_id,
        signa=sign,
        ts=ts,
        file_len=audio_file.size,
        file_name=audio_file.file_name,
        slice_num=slice_num,
        has_seperate=has_seperate,
        speaker_number=speaker_number
    )
    res = requests.post(url=url, data=params, headers=headers)
    res.encoding = Unicode.UTF_8.value
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    return res.json()


def upload_request(app_id, sign, ts, task_id, upload_file_path):
    """
    文件上传
    :param app_id:
    :param sign:
    :param ts:
    :param task_id:
    :param upload_file_path:
    :return:
    """
    # 文件分片大下52k
    file_piece_sice = 10485760
    url = 'http://raasr.xfyun.cn/api/upload'

    with open(upload_file_path, 'rb') as f:
        index = 1
        sig = SliceIdGenerator()
        while True:
            content = f.read(file_piece_sice)
            if not content or len(content) == 0:
                break
            files = {
                # "filename": self.gene_params(api_upload).get("slice_id"),
                'content': content
            }

            params = dict(
                app_id=app_id,
                signa=sign,
                ts=ts,
                task_id=task_id,
                slice_id=sig.get_next_slice_id()
            )

            res = requests.post(url=url, data=params, files=files)
            res.encoding = Unicode.UTF_8.value
            print(res.status_code)
            print(json.dumps(res.json(), indent=4, ensure_ascii=False))

            if res.json().get('ok') != 0:
                # 上传分片失败
                print('upload slice fail, response: ' + str(res))
                return False
            print('upload slice ' + str(index) + ' success')
            index += 1
        return True


def merge(app_id, sign, ts, task_id):
    """
    合并文件
    :param app_id:
    :param sign:
    :param ts:
    :param task_id:
    :return:
    """
    url = 'http://raasr.xfyun.cn/api/merge'

    params = dict(
        app_id=app_id,
        signa=sign,
        ts=ts,
        task_id=task_id
    )
    res = requests.post(url=url, data=params)
    res.encoding = Unicode.UTF_8.value
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    return res.json()


def get_progress(app_id, sign, ts, task_id):
    """
    查询处理进度
    :param app_id:
    :param sign:
    :param ts:
    :param task_id:
    :return:
    """
    url = 'http://raasr.xfyun.cn/api/getProgress'
    params = dict(
        app_id=app_id,
        signa=sign,
        ts=ts,
        task_id=task_id
    )
    res = requests.post(url=url, data=params)
    res.encoding = Unicode.UTF_8.value
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    return res.json()


def get_result(app_id, sign, ts, task_id):
    """
    获取结果
    :param app_id:
    :param sign:
    :param ts:
    :param task_id:
    :return:
    """
    url = 'http://raasr.xfyun.cn/api/getResult'
    params = dict(
        app_id=app_id,
        signa=sign,
        ts=ts,
        task_id=task_id
    )
    res = requests.post(url=url, data=params)
    res.encoding = Unicode.UTF_8.value
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    return res.json()


if __name__ == '__main__':
    app_id = '5b331864'
    api_key = '8ce5edee08cdce711d08fea808d55b00'
    file_path = 'D:/AIData/16k.wav'

    sign = 'TkrgxBS/KjOD+ZPz/G7K85KzRX4='
    ts = '1557913311'
    task_id = '0e9518942ef24e5a962e3e4481f2980a'
    # sign, ts = init_token(app_id, api_key)
    # print(sign, ts)
    # prepare(app_id, sign, ts, file_path)

    # upload_request(app_id, sign, ts, task_id, file_path)
    # merge(app_id, sign, ts, task_id)
    # get_progress(app_id, sign, ts, task_id)

    res_json = get_result(app_id, sign, ts, task_id)
    with open('D:/AIData/16k.txt', 'a') as f:
        for info in json.loads(res_json.get('data')):
            print(info)
            f.writelines(str(info) + '\n')
