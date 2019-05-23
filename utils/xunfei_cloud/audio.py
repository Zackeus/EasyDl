#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : audio.py 
# @Software: PyCharm
# @Time : 2019/5/15 16:08


import requests
import json
import math
from marshmallow import Schema, fields, post_load, pre_load

from utils import Unicode
from utils.xunfei_cloud.xunfei import Sign
from utils.object_util import is_not_empty, is_empty, BaseObject
from utils.decorators import auto_wired
from utils.errors import MyError
from utils.request import codes
from utils.assert_util import Assert


class Audio(BaseObject):

    # 文件分片大下52k
    __FILE_PIECE_SIZE = 10485760

    @auto_wired('utils.xunfei_cloud.audio.Audio')
    def __init__(self, app_id=None, api_key=None, sign=None, **kwargs):
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
        self.signa = sign.signa
        self.task_id = None

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def init_asr(self, task_id, ts, signa):
        """

        :param str task_id: 任务id
        :param str ts: 时间戳
        :param str signa: 数字签名
        :return:
        """
        self.task_id = task_id
        self.ts = ts
        self.signa = signa

    def asr(self, file_path, has_participle=False, has_seperate=True, speaker_number=2):
        """
        音频转写
        :param str file_path: 音频文件路径
        :param bool has_participle: 转写结果是否包含分词信息
        :param bool has_seperate: 转写结果中是否包含发音人分离信息
        :param int speaker_number: 发音人个数，可选值：0-10，0表示盲分
        :return:
        """
        from utils.file import Audio as BasicAudio
        has_participle = 'true' if has_participle else 'false'
        has_seperate = 'true' if has_seperate else 'false'
        audio_file = BasicAudio.probe(file_path)

        # 音频转写预处理
        prepare_info = self._asr_prepare(
            file_len=audio_file.size,
            file_name=audio_file.file_name,
            slice_num=math.ceil(audio_file.size / self.__FILE_PIECE_SIZE),
            has_participle=has_participle,
            has_seperate=has_seperate,
            speaker_number=speaker_number
        )
        Assert.is_true(prepare_info.ok == codes.success, prepare_info.failed, prepare_info.err_no)
        # 预处理成功，更新task_id
        self.task_id = prepare_info.data

        # 文件发片上传
        self._asr_upload(file_path)

        # 文件合并
        merge_info = self._asr_merge()
        Assert.is_true(merge_info.ok == codes.success, merge_info.failed, merge_info.err_no)

    def get_asr_progress(self):
        """
        查询音频转写处理进度
        :return:
        """
        url = getattr(self, 'asr_progress_url', None)
        data = dict(
            app_id=self.app_id,
            signa=self.signa,
            ts=self.ts,
            task_id=self.task_id
        )
        res = requests.post(url=url, data=data)
        res.encoding = Unicode.UTF_8.value

        if res is None or res.status_code != codes.ok:
            return AsrInfo(
                ok=codes.failed,
                err_no=res.status_code if res is not None else codes.bad,
                failed='查询音频转写处理进度请求失败'
            )
        progress_info, errors = AsrInfo.AsrInfoSchema().load(res.json())
        Assert.is_true(is_empty(errors), errors)
        if progress_info.ok == codes.success:
            progress_details, errors = AsrProgress.AsrProgressSchema().load(json.loads(progress_info.data))
            Assert.is_true(is_empty(errors), errors)
            progress_info.data = progress_details
        return progress_info

    def get_asr_result(self):
        """
        查询音频转写结果
        :return:
        """
        url = getattr(self, 'asr_result_url', None)
        data = dict(
            app_id=self.app_id,
            signa=self.signa,
            ts=self.ts,
            task_id=self.task_id
        )
        res = requests.post(url=url, data=data)
        res.encoding = Unicode.UTF_8.value

        if res is None or res.status_code != codes.ok:
            return AsrInfo(
                ok=codes.failed,
                err_no=res.status_code if res is not None else codes.bad,
                failed='查询音频转写结果请求失败'
            )
        result_info, errors = AsrInfo.AsrInfoSchema().load(res.json())
        Assert.is_true(is_empty(errors), errors)
        return result_info

    def _asr_prepare(self, **kwargs):
        """
        音频转写预处理
        :return:
        """
        url = getattr(self, 'asr_prepare_url', None)

        kwargs.update(dict(app_id=self.app_id, signa=self.signa, ts=self.ts))

        res = requests.post(url=url, data=kwargs)
        res.encoding = Unicode.UTF_8.value

        if res is None or res.status_code != codes.ok:
            return AsrInfo(
                ok=codes.failed,
                err_no=res.status_code if res is not None else codes.bad,
                failed='音频转写预处理请求失败'
            )
        prepare_info, errors = AsrInfo.AsrInfoSchema().load(res.json())
        Assert.is_true(is_empty(errors), errors)
        return prepare_info

    def _asr_upload(self, upload_file_path):
        """
        音频转写文件分片上传
        :param upload_file_path: 待上传音频文件路径
        :return:
        """
        url = getattr(self, 'asr_upload_url', None)
        sig = SliceIdGenerator()

        with open(upload_file_path, 'rb') as f:
            while True:
                content = f.read(self.__FILE_PIECE_SIZE)
                if not content or len(content) == 0:
                    break

                data = dict(
                    app_id=self.app_id,
                    signa=self.signa,
                    ts=self.ts,
                    task_id=self.task_id,
                    slice_id=sig.get_next_slice_id()
                )

                res = requests.post(url=url, data=data, files={'content': content})
                res.encoding = Unicode.UTF_8.value

                if res is None or res.status_code != codes.ok:
                    return AsrInfo(
                        ok=codes.failed,
                        err_no=res.status_code if res is not None else codes.bad,
                        failed='音频转写文件分片上传请求失败'
                    )
                upload_info, errors = AsrInfo.AsrInfoSchema().load(res.json())
                Assert.is_true(is_empty(errors), errors)

                # 上传分片失败
                Assert.is_true(
                    upload_info.ok == codes.success,
                    upload_info.err_no,
                    '分片上传失败：{0}'.format(upload_info.failed)
                )

    def _asr_merge(self):
        """
        音频转写文件合并
        :return:
        """
        url = getattr(self, 'asr_merge_url', None)

        data = dict(
            app_id=self.app_id,
            signa=self.signa,
            ts=self.ts,
            task_id=self.task_id
        )
        res = requests.post(url=url, data=data)
        res.encoding = Unicode.UTF_8.value

        if res is None or res.status_code != codes.ok:
            return AsrInfo(
                ok=codes.failed,
                err_no=res.status_code if res is not None else codes.bad,
                failed='音频转写文件合并请求失败'
            )
        merge_info, errors = AsrInfo.AsrInfoSchema().load(res.json())
        Assert.is_true(is_empty(errors), errors)
        return merge_info


class AsrInfo(BaseObject):

    def __init__(self, ok, err_no, failed=None, data=None, task_id=None):
        """
        音频转写返回结果
        :param int ok: 调用成功标志（0：成功，-1：失败）
        :param int err_no: 错误码
        :param str failed: 错误描述（null：未出错）
        :param str data: 数据，具体含义见各接口返回说明（null：无返回值）
        :param str task_id: 任务id，此字段只在主动回调的结果中存在
        """
        self.ok = ok
        self.err_no = err_no
        self.failed = failed
        self.data = data
        self.task_id = task_id

    class AsrInfoSchema(Schema):
        ok = fields.Integer(required=True)
        err_no = fields.Integer(required=True)
        failed = fields.Str()
        data = fields.Str()
        task_id = fields.Str()

        @pre_load
        def pre_load_data(self, pre_data):
            for key in list(pre_data.keys()):
                if pre_data.get(key, None) is None:
                    pre_data.pop(key)
            return pre_data

        @post_load
        def make_object(self, data):
            return AsrInfo(**data)


class AsrProgress(BaseObject):

    def __init__(self, status, desc):
        """
        音频转写查询进度
        :param int status: 状态 仅当任务状态=9（转写结果上传完成），才可调用获取结果接口获取转写结果
        :param str desc: 描述
        """
        self.status = status
        self.desc = desc

    class AsrProgressSchema(Schema):
        status = fields.Integer(required=True)
        desc = fields.Str(required=True)

        @post_load
        def make_object(self, data):
            return AsrProgress(**data)


class SliceIdGenerator(BaseObject):

    def __init__(self):
        """
        slice id生成器
        """
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
