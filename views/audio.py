#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : audio.py 
# @Software: PyCharm
# @Time : 2019/5/30 9:17


import json
import requests
from flask import Blueprint, render_template

from models.audio import AudioLexerModel, AudioLexerSchema
from utils import Method, ContentType, render_info, MyResponse, validated

audio_bp = Blueprint('audio', __name__)


@audio_bp.route('/lexer', methods=[Method.POST.value])
@validated(AudioLexerSchema, only=AudioLexerSchema().only_create(), consumes=ContentType.JSON.value)
def add_lexer(audio_lexer):
    """
    新增词性分析
    :param AudioLexerModel audio_lexer:
    :return:
    """
    audio_lexer.dao_create()
    return render_info(MyResponse(msg='添加成功'))


@audio_bp.route('asr_nlp')
def asr_nlp():
    """
    音频转写加词性分析
    :return:
    """
    from utils import Assert, is_empty, is_not_empty
    from utils.file import AudioAsrNlp
    result = []
    with open('D:/AIData/音频转写/0850487/0850487_lexer.txt', 'r') as f:
        for line in f.readlines():
            result.append(json.loads(line.strip('\n').replace("'", "\"")))

    asr_nlp_datas, errors = AudioAsrNlp.AudioAsrNlpSchema().load(result, many=True)
    Assert.is_true(is_empty(errors), errors)

    ne_list = []
    for asr_nlp_data in asr_nlp_datas:
        if is_not_empty(asr_nlp_data.ne_list):
            ne_list.extend(asr_nlp_data.ne_list)

    # 查询识别出的词性列表
    audio_lexers = AudioLexerModel().dao_get_by_codes(ne_list)
    return render_template('audio/asr_nlp.html', asr_nlp_datas=asr_nlp_datas, audio_lexers=audio_lexers)


if __name__ == '__main__':
    data = {
        'code': 'TOA',
        'title': '汽车品牌',
        'color': '#CC0000'
    }
    url = 'http://127.0.0.1:5000/audio/lexer'
    res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    print(res)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
