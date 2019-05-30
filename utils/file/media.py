#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 多媒体工具类 底层需要 ffmpeg 的支持
# @Author : Zackeus
# @File : media.py
# @Software: PyCharm
# @Time : 2019/5/9 14:48


import os
import ffmpeg
from enum import Enum, unique
from marshmallow import Schema, fields, post_load

from utils.file.file import FileUtil, FileFormat
from utils.assert_util import Assert
from utils.object_util import is_not_empty, is_empty, BaseObject
from utils.xunfei_cloud.audio import AsrData
from utils.baidu_cloud.nlp import LexerItem


@unique
class AudioFormat(Enum):
    """
    支持的音频封装格式 (也就是-f后面可以接的参数4Y)
    """
    AVI = 'avi'
    F32BE = 'f32be'  # PCM 32-bit floating-point big-endian
    F32LE = 'f32le'  # PCM 32-bit floating-point little-endian
    F64BE = 'f64be'  # PCM 64-bit floating-point big-endian
    F64LE = 'f64le'  # PCM 64-bit floating-point little-endian
    MP2 = 'mp2'      # MP2 (MPEG audio layer 2)
    MP3 = 'mp3'      # MP3 (MPEG audio layer 3)
    MP4 = 'mp4'      # MP4 (MPEG-4 Part 14)
    S16BE = 's16be'  # PCM signed 16-bit big-endian
    S16LE = 's16le'  # PCM signed 16-bit little-endian
    S24BE = 's24be'  # PCM signed 24-bit big-endian
    S24LE = 's24le'  # PCM signed 24-bit little-endian
    S32BE = 's32be'  # PCM signed 32-bit big-endian
    S32LE = 's32le'  # PCM signed 32-bit little-endian
    S337M = 's337m'  # SMPTE 337M
    S8 = 's8'        # PCM signed 8-bit
    U16BE = 'u16be'  # PCM unsigned 16-bit big-endian
    U16LE = 'u16le'  # PCM unsigned 16-bit little-endian
    U24BE = 'u24be'  # PCM unsigned 24-bit big-endian
    U24LE = 'u24le'  # PCM unsigned 24-bit little-endian
    U32BE = 'u32be'  # PCM unsigned 32-bit big-endian
    U32LE = 'u32le'  # PCM unsigned 32-bit little-endian
    U8 = 'u8'        # PCM unsigned 8-bit
    WAV = 'wav'      # WAV / WAVE (Waveform Audio)


@unique
class AudioCodecs(Enum):
    """
    支持的音频编码器 (也就是-acodec后面可以接的参数)
    """
    MP2 = 'mp2'                # MP2 (MPEG audio layer 2) (decoders: mp2 mp2float ) (encoders: mp2 mp2fixed libtwolame )
    MP3 = 'mp3'                # MP3 (MPEG audio layer 3) (decoders: mp3float mp3 ) (encoders: libmp3lame libshine )
    PCM_ALAW = 'pcm_alaw'      # PCM A-law / G.711 A-law
    PCM_BLURAY = 'pcm_bluray'  # PCM signed 16|20|24-bit big-endian for Blu-ray media
    PCM_DVD = 'pcm_dvd'        # PCM signed 20|24-bit big-endian
    PCM_F16LE = 'pcm_f16le'    # PCM 16.8 floating point little-endian
    PCM_F24LE = 'pcm_f24le'    # PCM 24.0 floating point little-endian
    PCM_F32BE = 'pcm_f32be'    # PCM 32-bit floating point big-endian
    PCM_F32LE = 'pcm_f32le'    # PCM 32-bit floating point little-endian
    PCM_F64BE = 'pcm_f64be'    # PCM 64-bit floating point big-endian
    PCM_F64LE = 'pcm_f64le'    # PCM 64-bit floating point little-endian
    PCM_S16BE = 'pcm_s16be'    # PCM 16.8 floating point little-endian
    PCM_S16LE = 'pcm_s16le'    # PCM signed 16-bit little-endian


class Audio(BaseObject):

    __FORMAT = [FileFormat.PCM.value, FileFormat.MP3.value, FileFormat.WAV.value,
                FileFormat.V3.value]

    def __init__(self, file_name, codec_type, codec_name, codec_long_name, format_name, format_long_name,
                 sample_rate, channels, duration, size):
        """
        音频文件
        :param str file_name: 文件名称（带后缀）
        :param str codec_type: 编码类型
        :param str codec_name: 编码名称
        :param str codec_long_name: 编码全名
        :param str format_name: 格式名称
        :param str format_long_name: 格式全名
        :param int sample_rate: 采样率
        :param int channels: 声道数
        :param float duration: 总时长
        :param long size: 字节大小
        """
        self.file_name = file_name
        self.codec_type = codec_type
        self.codec_name = codec_name
        self.codec_long_name = codec_long_name
        self.format_name = format_name
        self.format_long_name = format_long_name
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        self.size = size

    @classmethod
    def probe(cls, file_path, is_ffprobe=True):
        """
        解析音频文件参数
        :param is_ffprobe: 是否使用 ffprobe 解析文件格式
        :param file_path:
        :return:
        :rtype: Audio
        """
        Assert.is_true(os.path.isfile(file_path), '文件不存在：{0}'.format(file_path))
        _, file_name, format_name = FileUtil.get_path_name_ext(file_path)

        probe_json = ffmpeg.probe(file_path)
        audio_json = probe_json.get('streams')[0]
        audio_json.update(probe_json.get('format'))
        audio_json.update({'file_name': '{name}.{ext}'.format(name=file_name, ext=format_name)})
        audio, errors = AudioSchema().load(audio_json)
        Assert.is_true(is_empty(errors), errors)

        if not is_ffprobe:
            audio.format_name = format_name
        return audio

    @classmethod
    def is_pcm(cls, file_path, is_strict=True):
        """
        判断是否为 pcm 拓展文件
        :param file_path: 文件路径
        :param is_strict:
        :return:
        """
        _, _, file_ext = FileUtil.get_path_name_ext(file_path, is_strict=is_strict)
        return file_ext.upper() == FileFormat.PCM.value

    @classmethod
    def is_mp3(cls, file_path, is_strict=True):
        """
        判断是否为 mp3 拓展文件
        :param file_path: 文件路径
        :param is_strict:
        :return:
        """
        _, _, file_ext = FileUtil.get_path_name_ext(file_path, is_strict=is_strict)
        return file_ext.upper() == FileFormat.MP3.value

    @classmethod
    def is_wav(cls, file_path, is_strict=True):
        """
        判断是否为 wav 拓展文件
        :param file_path: 文件路径
        :param is_strict:
        :return:
        """
        _, _, file_ext = FileUtil.get_path_name_ext(file_path, is_strict=is_strict)
        return file_ext.upper() == FileFormat.WAV.value

    @classmethod
    def _file_args(cls, format=None, acodec=None, ac=None, ar=None):
        """
        音频文件参数信息
        :param str format: 格式
        :param str acodec: 编码器
        :param int ac: 声道数
        :param int ar: 采样率
        :return:
        """
        file_dict_args = {}
        if is_not_empty(format):
            file_dict_args['format'] = format
        if is_not_empty(acodec):
            file_dict_args['acodec'] = acodec
        if is_not_empty(ac):
            file_dict_args['ac'] = ac
        if is_not_empty(ar):
            file_dict_args['ar'] = ar
        return file_dict_args

    @classmethod
    def _format_convert(cls, input_file, output_file, output_ac, output_ar,
                        input_ac=None, input_ar=None,
                        input_format=None, input_acodec=None,
                        output_format=None, output_acodec=None):
        """
        音频文件格式转换
        :param input_file:
        :param output_file:
        :param output_ac:
        :param output_ar:
        :param input_ac:
        :param input_ar:
        :param input_format:
        :param input_acodec:
        :param output_format:
        :param output_acodec:
        :return:
        """
        output_dir, _, _ = FileUtil.get_path_name_ext(output_file, is_strict=False)
        FileUtil.creat_dirs(output_dir)

        if cls.is_pcm(input_file):
            # 格式为 pcm 格式，需要音频文件参数
            Assert.is_true((is_not_empty(input_ac) and is_not_empty(input_ar) and is_not_empty(input_format)
                            and is_not_empty(input_acodec)), 'pcm 缺失文件参数')

        _, error = (ffmpeg.input(input_file, **cls._file_args(input_format, input_acodec, input_ac, input_ar)).
                    output(output_file, **cls._file_args(output_format, output_acodec, output_ac, output_ar)).
                    run(capture_stdout=False, overwrite_output=True))

    @classmethod
    def to_pcm(cls, input_file, output_file, output_ac, output_ar,
               input_ac=None, input_ar=None, input_format=None, input_acodec=None,
               output_format=AudioFormat.S16LE.value, output_acodec=AudioCodecs.PCM_S16LE.value):
        """
        转 pcm 格式音频
        :param str input_file: 待转换文件路径
        :param int input_ac: 输入声道数（pcm 格式需要）
        :param int input_ar: 输入采样率 （pcm 格式需要）
        :param str input_format: 输入格式 （pcm 格式需要）
        :param str input_acodec: 输入编码器 （pcm 格式需要）
        :param str output_file: 转换输出文件路径
        :param int output_ac: 输出声道数
        :param int output_ar: 输出采样率
        :param str output_format: 输出格式
        :param str output_acodec: 输出编码器
        :return:
        """
        Assert.is_true(cls.is_pcm(output_file, is_strict=False), '不是 pcm 拓展文件：{0}'.format(output_file))
        cls._format_convert(input_file=input_file, output_file=output_file,
                            input_format=input_format, input_acodec=input_acodec,
                            input_ac=input_ac, input_ar=input_ar,
                            output_format=output_format, output_acodec=output_acodec,
                            output_ac=output_ac, output_ar=output_ar)

    @classmethod
    def to_mp3(cls, input_file, output_file, output_ac, output_ar,
               input_ac=None, input_ar=None, input_format=None, input_acodec=None):
        """
        转 mp3 格式音频
        :param str input_file: 待转换文件路径
        :param str output_file:
        :param int output_ac:
        :param int output_ar:
        :param int input_ac:
        :param int input_ar:
        :param str input_format:
        :param str input_acodec:
        :return:
        """
        Assert.is_true(cls.is_mp3(output_file, is_strict=False), '不是 mp3 拓展文件：{0}'.format(output_file))
        cls._format_convert(input_file=input_file, output_file=output_file,
                            input_format=input_format, input_acodec=input_acodec,
                            input_ac=input_ac, input_ar=input_ar,
                            output_ac=output_ac, output_ar=output_ar)

    @classmethod
    def to_wav(cls, input_file, output_file, output_ac, output_ar,
               input_ac=None, input_ar=None, input_format=None, input_acodec=None):
        """
        转 wav 格式音频
        :param input_file:
        :param output_file:
        :param output_ac:
        :param output_ar:
        :param input_ac:
        :param input_ar:
        :param input_format:
        :param input_acodec:
        :return:
        """
        Assert.is_true(cls.is_wav(output_file, is_strict=False), '不是 wav 拓展文件：{0}'.format(output_file))
        cls._format_convert(input_file=input_file, output_file=output_file,
                            input_format=input_format, input_acodec=input_acodec,
                            input_ac=input_ac, input_ar=input_ar,
                            output_ac=output_ac, output_ar=output_ar)


class AudioSchema(Schema):

    file_name = fields.Str()
    codec_type = fields.Str()
    codec_name = fields.Str()
    codec_long_name = fields.Str()
    format_name = fields.Str()
    format_long_name = fields.Str()
    sample_rate = fields.Integer()
    channels = fields.Integer()
    duration = fields.Float()
    size = fields.Integer()

    @post_load
    def make_object(self, data):
        return Audio(**data)


class AudioAsrNlp(AsrData):

    def __init__(self, bg, ed, onebest, speaker, items):
        """
        音频转写+词性分析
        :param long bg: 句子相对于本音频的起始时间，单位为ms
        :param long ed: 句子相对于本音频的终止时间，单位为ms
        :param str onebest: 句子内容
        :param int speaker: 说话人编号，从1开始，未开启说话人分离时speaker都为0
        :param list items: 词汇数组，每个元素对应结果中的一个词
        """
        super(self.__class__, self).__init__(bg, ed, onebest, speaker)
        self.items = items
        # 命名实体列表
        self.ne_list = []

        for item in items:
            if item.ne not in self.ne_list:
                self.ne_list.append(item.ne)

    class AudioAsrNlpSchema(AsrData.AsrDataSchema):

        items = fields.Nested(
            LexerItem.LexerItemSchema,
            required=True,
            many=True
        )

        @post_load
        def make_object(self, data):
            return AudioAsrNlp(**data)


if __name__ == '__main__':
    # print(Audio.probe('D:/AIData/16k.wav', is_ffprobe=False))

    # v3 转换单声道，8k采样率，16bits采样点，pcm
    # Audio.to_pcm('D:/AIData/0850487.V3', 'D:/AIData/8k.pcm', 1, 8000)

    # 单声道，8k采样率，16bits采样点，pcm 转 2声道，16k采样率，16bits采样点，pcm
    # Audio.to_pcm(input_file='D:/AIData/8k.pcm',
    #              input_format=AudioFormat.S16LE.value,
    #              input_acodec=AudioCodecs.PCM_S16LE.value,
    #              input_ac=1, input_ar=8000,
    #              output_file='D:/AIData/16k.pcm', output_ac=2, output_ar=16000)

    # v3 转 mp3
    # Audio.to_mp3('D:/AIData/0850487.V3', 'D:/AIData/0850487.mp3', output_ac=2, output_ar=44100)

    # v3 转 wav
    Audio.to_wav('D:/AIData/1334006.V3', 'D:/AIData/1334006.wav', output_ac=2, output_ar=16000)


# ffmpeg -y -f s16le -ar 8000 -ac 1 -i D:/AIData/16k.pcm -ar 44100 -ac 2 D:/AIData/16k.wav
# ffmpeg -y -i D:/AIData/0850487.V3 -ar 44100 -ac 2 D:/AIData/16k.wav

# wav 文件转 16k 16bits 位深的单声道pcm文件
# ffmpeg -y  -i 16k.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm

# 44100 采样率 单声道 16bts pcm 文件转 16000采样率 16bits 位深的单声道pcm文件
# ffmpeg -y -f s16le -ac 1 -ar 44100 -i test44.pcm  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm

# mp3 文件转 16K 16bits 位深的单声道 pcm文件
# ffmpeg -y  -i aidemo.mp3  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm

# -acodec pcm_s16le pcm_s16le 16bits 编码器
# -f s16le 保存为16bits pcm格式
# -ac 1 单声道
# -ar 16000  16000采样率

# 使用ffplay播放频率为44100Hz，双通道，16位、小端的音频文件audio1.pcm
# ffplay -ar 44100 -ac 2 -f s16le -i audio1.pcm








