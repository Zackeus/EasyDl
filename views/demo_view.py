#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : test.py 
# @Software: PyCharm
# @Time : 2019/4/8 13:33


import os
from flask import Blueprint, render_template
from extensions import db

from utils import Method
from utils.file import FileUtil


demo_bp = Blueprint('demo', __name__)


@demo_bp.route('/file_scan', methods=[Method.GET.value])
def file_scan():
    return render_template('demo/file_scan.html')


@demo_bp.route('/upload_md5', methods=[Method.GET.value])
def upload_md5():
    return render_template('demo/upload_md5.html')


@demo_bp.route('/context', methods=[Method.GET.value])
def context():
    return render_template('demo/context.html')


@demo_bp.route('/data/<string:date>')
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





