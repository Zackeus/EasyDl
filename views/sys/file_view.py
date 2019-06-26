#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : file_view.py 
# @Software: PyCharm
# @Time : 2019/6/19 14:16


from flask import Blueprint

from models import FileModel
from utils import Method, is_empty
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
