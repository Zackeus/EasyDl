#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : file_view.py 
# @Software: PyCharm
# @Time : 2019/6/19 14:16


from flask import Blueprint, request

from models import FileModel
from utils import Method, is_empty, render_json, MyResponse
from utils.sys import download_file


file_bp = Blueprint('file', __name__)


@file_bp.route('/<string:id>/<string:md5_id>', methods=[Method.GET.value])
@file_bp.route('/<string:id>/<string:md5_id>/<string:as_attachment>', methods=[Method.GET.value])
def file_download(id, md5_id, as_attachment=None):
    """
    文件下载
    :param id:
    :param md5_id:
    :param as_attachment:
    :return:
    """
    as_attachment = True if is_empty(as_attachment) else False
    file = FileModel().dao_down_file(id, md5_id)  # type: FileModel
    return download_file(file.file_path,
                         '{0}.{1}'.format(file.file_name, file.file_format),
                         as_attachment=as_attachment)


@file_bp.route('', methods=[Method.POST.value])
def file_upload():
    """
    文件上传
    :return:
    """
    file = request.files.get('file')
    print(type(file))
    print(file.filename)

    if file.filename == '4.JPG':
        return render_json(MyResponse('上传成功', code='22'))
    return render_json(MyResponse('上传成功'))