#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : audio.py 
# @Software: PyCharm
# @Time : 2019/5/30 9:17


import json
import requests
from flask import Blueprint, render_template, url_for

from models.audio import AudioLexerNeModel, AudioLexerNeSchema
from utils import Method, ContentType, render_info, MyResponse, validated

audio_bp = Blueprint('audio', __name__)


@audio_bp.route('/lexer_ne', methods=[Method.POST.value])
@validated(AudioLexerNeSchema, only=AudioLexerNeSchema().only_create(), consumes=ContentType.JSON.value)
def add_lexer_ne(audio_lexer_ne):
    """
    新增词性分析
    :param AudioLexerModel audio_lexer_ne:
    :return:
    """
    audio_lexer_ne.dao_create()
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

    # 查询识别出的词性列表, 单词性
    # ne_list = []
    # for asr_nlp_data in asr_nlp_datas:
    #     if is_not_empty(asr_nlp_data.ne_list):
    #         ne_list.extend(asr_nlp_data.ne_list)
    # audio_lexers = AudioLexerNeModel().dao_get_by_codes(ne_list)

    # ***********************************

    items = []
    for asr_nlp_data in asr_nlp_datas:
        for item in asr_nlp_data.items:
            items.append(item)

    audio_lexers = AudioLexerNeModel().dao_get_all()
    for audio_lexer in audio_lexers:
        audio_lexer.items = []
        for item in items:
            if audio_lexer.code == item.ne:
                audio_lexer.items.append(item)

    # 移除 item 为空的标签栏
    for audio_lexer in audio_lexers.copy():
        if is_empty(audio_lexer.items):
            audio_lexers.remove(audio_lexer)

    return render_template(
        'audio/asr_nlp.html',
        audio_src=url_for('static', filename='songs/{id}.wav'.format(id=id)),
        asr_nlp_datas=asr_nlp_datas,
        audio_lexers=audio_lexers
    )


@audio_bp.route('/xunfei/asr/<string:id>')
def xunfei_asr(id):
    """
    讯飞音频转写
    :param id:
    :return:
    """
    import os
    from utils.xunfei_cloud.audio import Audio
    audio = Audio()
    audio.asr(file_path=os.path.join('D:/AIData/音频转写', id, '{id}.wav'.format(id=id)))
    audio.get_asr_progress()
    print(audio.task_id, audio.signa, audio.ts)
    return 'ok'


@audio_bp.route('/xunfei/asr_progress/<string:id>/<string:task_id>/<string:ts>/<path:signa>')
def xunfei_asr_progress(id, task_id, ts, signa):
    """
    讯飞音频转写结果查询
    :param id:
    :param task_id:
    :param ts:
    :param signa:
    :return:
    """
    import os
    from utils.xunfei_cloud.audio import Audio
    from utils import codes, Assert
    audio = Audio()
    audio.init_asr(task_id, ts, signa)
    asr_progress = audio.get_asr_progress()

    if asr_progress.ok == codes.success and asr_progress.data.status == codes.asr_success:
        asr_result = audio.get_asr_result()
        Assert.is_true(asr_result.ok == codes.success, asr_result.failed)

        with open(os.path.join('D:/AIData/音频转写', id, '{id}.txt'.format(id=id)), 'a') as f:
            for info in json.loads(asr_result.data):
                print(info)
                f.writelines(str(info) + '\n')
    else:
        print(asr_progress.failed if asr_progress.ok != codes.success else asr_progress.data.desc)
    return 'ok'


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
    print(111111111111)
    ne_list = AudioLexerNeModel().dao_get_codes()
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
            print(lexer_json)
            asr_json.update({'items': lexer_json.get('items', [])})
            result.append(asr_json)

    with open(os.path.join(file_dir, id, file_lexer_name), 'a') as f:
        for info in result:
            print(info)
            f.writelines(str(info) + '\n')
    return 'ok'


if __name__ == '__main__':
    data = {
        'code': 'MS',
        'title': '婚姻状态',
        'color': '#984B4B'
    }
    url = 'http://127.0.0.1:5000/audio/lexer_ne'
    res = requests.post(url=url, json=data, headers=ContentType.JSON_UTF8.value)

    print(res)
    print(res.status_code)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))
