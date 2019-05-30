#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : test.py 
# @Software: PyCharm
# @Time : 2019/4/8 13:33


import json
import os
from flask import Blueprint, make_response, send_from_directory, request, current_app
from extensions import db

from utils import Method, IdGen
from utils.file import FileUtil


test_bp = Blueprint('test', __name__)


@test_bp.route('/data/<string:date>')
def data(date):
    """
    图片数据分类
    :return:
    """
    base_dir = os.path.join('D:/AIData', date)
    data_dir = os.path.join(base_dir, 'DATA')
    file_lists = FileUtil.get_files_by_suffix(base_dir, ['JPG', 'JPEG', 'PNG'])
    for file in file_lists:
        _, file_id, file_ext = FileUtil.get_path_name_ext(file)

        with db.auto_commit_db() as s:
            sql = "SELECT FILE_TYPE FROM ( " \
                  "SELECT DISTINCT " \
                  "SUBSTR(J.BIZ_TYPE, INSTR(J.BIZ_TYPE, '_', -1) + 1) AS FILE_TYPE " \
                  "FROM js_sys_file_upload J " \
                  "INNER JOIN ucl_loan_file_code U ON SUBSTR(J.BIZ_TYPE, INSTR(J.BIZ_TYPE, '_',-1) + 1) = U.FILE_CODE " \
                  "WHERE FILE_ID = :file_id " \
                  "order by FILE_TYPE) " \
                  "WHERE ROWNUM = 1"
            res = s.execute(sql, params={'file_id': file_id}, bind=db.get_engine(bind='YFC_UCL_PRD'))
            res = res.cursor.fetchone()
            if res:
                file_type = res[0]
            else:
                file_type = 'default'

            FileUtil.copy_file(file, os.path.join(data_dir, file_type))
    print('OVER *******************************')
    return date


@test_bp.route('audio')
def audio():
    """
    百度音频转写
    :return:
    """
    from utils.baidu_cloud import Audio
    audio_cls = Audio()
    return audio_cls.offline_transfer(IdGen.uuid())


@test_bp.route('/download/<string:call_id>')
def download_file(call_id):
    """
    下载音频文件
    :param call_id:
    :return:
    """
    print(call_id)
    file_name = '8k.pcm'
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    response = make_response(send_from_directory('D:/AIData', file_name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".\
        format(file_name.encode().decode('latin-1'))
    return response


@test_bp.route('/call_back', methods=[Method.POST.value])
def call_back():
    """
    百度音频文件转写识别回调
    :return:
    """
    current_app.logger.error(json.dumps(request.json(), indent=4, ensure_ascii=False))


@test_bp.route('xunfei/audio')
def xunfei_audio():
    """
    讯飞音频转写
    :return:
    """
    from utils.xunfei_cloud.audio import Audio
    from utils import codes, Assert
    # audio = Audio()
    # audio.asr(file_path='D:/AIData/1334006.wav')
    # audio.get_asr_progress()
    # print(audio.task_id, audio.signa, audio.ts)

    audio = Audio()
    audio.init_asr('b2f842c81f454b69a8ef0ba345d36071', '1558510114', 'EoUu8ZaC47tpofHKwA+hIonz5xc=')
    asr_progress = audio.get_asr_progress()

    if asr_progress.ok == codes.success and asr_progress.data.status == codes.asr_success:
        asr_result = audio.get_asr_result()
        Assert.is_true(asr_result.ok == codes.success, asr_result.failed)

        with open('D:/AIData/1334006.txt', 'a') as f:
            for info in json.loads(asr_result.data):
                print(info)
                f.writelines(str(info) + '\n')
    else:
        print(asr_progress.failed if asr_progress.ok != codes.success else asr_progress.data.desc)

    return 'ok'


@test_bp.route('/baidu/nlp')
def baidu_nlp():
    """
    百度自然语言处理
    :return:
    """
    from utils.baidu_cloud import NLP, LexerRes
    from utils import Assert, is_empty
    ne_list = ['PER', 'LOC', 'ORG', 'TIME', 'TBW', 'TOA', ]
    result = []

    nlp = NLP()
    with open('D:/AIData/0850487.txt', 'r') as f:
        for line in f.readlines():
            asr_json = json.loads(line.strip('\n').replace("'", "\""))
            lexer_res = nlp.lexer(text=asr_json.get('onebest', ''), ne_list=ne_list)

            lexer_json, errors = LexerRes.LexerResSchema().dump(lexer_res)
            Assert.is_true(is_empty(errors), errors)
            asr_json.update({'items': lexer_json.get('items', [])})
            result.append(asr_json)

    with open('D:/AIData/0850487_lexer.txt', 'a') as f:
        for info in result:
            print(info)
            f.writelines(str(info) + '\n')
    return 'ok'
