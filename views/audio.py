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


@audio_bp.route('asr_nlp/<string:id>')
def asr_nlp(id):
    """
    音频转写加词性分析
    :param id:
    :return:
    """
    import os
    from utils import Assert, is_empty, is_not_empty
    from utils.file import AudioAsrNlp
    result = []
    with open(os.path.join('D:/AIData/音频转写', id, '{id}_lexer.txt'.format(id=id)), 'r') as f:
        for line in f.readlines():
            result.append(json.loads(line.strip('\n').replace("'", "\"")))

    asr_nlp_datas, errors = AudioAsrNlp.AudioAsrNlpSchema().load(result, many=True)
    Assert.is_true(is_empty(errors), errors)

    # 查询识别出的词性列表
    ne_list = []
    for asr_nlp_data in asr_nlp_datas:
        if is_not_empty(asr_nlp_data.ne_list):
            ne_list.extend(asr_nlp_data.ne_list)
    audio_lexers = AudioLexerModel().dao_get_by_codes(ne_list)
    return render_template('audio/asr_nlp.html', asr_nlp_datas=asr_nlp_datas, audio_lexers=audio_lexers)


@audio_bp.route('/baidu/nlp/<string:id>')
def baidu_nlp(id):
    """
    百度自然语言处理
    :param id:
    :return:
    """
    import os
    from utils.baidu_cloud import NLP, LexerRes
    from utils import Assert, is_empty
    ne_list = AudioLexerModel().dao_get_codes()
    result = []

    nlp = NLP()
    file_dir = 'D:/AIData/音频转写'
    file_name = '{id}.txt'.format(id=id)
    file_lexer_name = '{id}_lexer.txt'.format(id=id)
    with open(os.path.join(file_dir, id, file_name), 'r') as f:
        for line in f.readlines():
            asr_json = json.loads(line.strip('\n').replace("'", "\""))
            lexer_res = nlp.lexer(text=asr_json.get('onebest', ''), ne_list=ne_list)

            lexer_json, errors = LexerRes.LexerResSchema().dump(lexer_res)
            Assert.is_true(is_empty(errors), errors)
            asr_json.update({'items': lexer_json.get('items', [])})
            result.append(asr_json)

    with open(os.path.join(file_dir, id, file_lexer_name), 'a') as f:
        for info in result:
            print(info)
            f.writelines(str(info) + '\n')
    return 'ok'


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
