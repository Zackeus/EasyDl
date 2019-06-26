#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 视图工具类
# @Author : Zackeus
# @File : views_util.py 
# @Software: PyCharm
# @Time : 2019/6/19 15:13


from flask import make_response, send_from_directory

from utils import Unicode
from utils.file import FileUtil


def download_file(file_path, file_name, as_attachment=True):
    """
    文件下载
    :param file_path: 文件路径
    :param file_name: 文件名
    :param bool as_attachment: 是否作为附件，为false时去除 Content-Disposition 头部信息
    :return:
    """

    file_path, name, ext = FileUtil.get_path_name_ext(file_path, False)

    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    response = make_response(send_from_directory(file_path, '{0}.{1}'.format(name, ext), as_attachment=as_attachment))

    if as_attachment:
        response.headers["Content-Disposition"] = "attachment; filename={}".\
            format(file_name.encode().decode(Unicode.LATIN_1.value))
    return response


