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
    from utils.baidu_cloud import Audio
    audio_cls = Audio()
    return audio_cls.offline_transfer(IdGen.uuid())


@test_bp.route('/download/<string:call_id>')
def download_file(call_id):
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
    音频文件转写识别回调
    :return:
    """
    current_app.logger.error(json.dumps(request.json(), indent=4, ensure_ascii=False))


@test_bp.route('xunfei/audio')
def xunfei_audio():
    from utils.xunfei_cloud.audio import Audio
    audio = Audio()
    print(audio)
    return 'ok'

