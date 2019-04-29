#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : file.py
# @Software: PyCharm
# @Time : 2019/3/26 9:41


import glob
import os.path
import shutil
import requests
import hashlib
import base64
from utils.errors import MyError
from utils.assert_util import Assert
from enum import Enum, unique


_curdir = os.curdir
_sep = os.sep
_altsep = os.altsep


class FileUtil:

    @staticmethod
    def get_sha1_path(file_path, block_size=64 * 1024, hexadecimal=True, b64=False):
        """
        计算文件的sha1值
        :param file_path: 文件路径
        :param block_size: 批次读取size大小
        :param hexadecimal: 是否使用十六进制，否则使用二进制
        :param b64: 是否 base64 编码
        :return:
        """
        from utils.encodes import hash_code

        Assert.is_true(os.path.isfile(file_path), '文件不存在, path: {0}'.format(file_path))
        with open(file_path, 'rb') as f:
            sha1 = hashlib.sha1()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                sha1.update(data)
            return hash_code(sha1, hexadecimal, b64)

    @staticmethod
    def get_md5_path(file_path, block_size=64 * 1024, hexadecimal=True, b64=False):
        """
        获取文件 md5
        :param file_path: 文件路径
        :param block_size: 批次读取size大小
        :param hexadecimal: 是否使用十六进制，否则使用二进制
        :param b64: 是否 base64 编码
        :return:
        """
        from utils.encodes import hash_code

        Assert.is_true(os.path.isfile(file_path), '文件不存在, path: {0}'.format(file_path))
        with open(file_path, 'rb') as f:
            md5 = hashlib.md5()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
            return hash_code(md5, hexadecimal, b64)

    @staticmethod
    def get_sha1_b64(file_b64, hexadecimal=True, b64=False):
        """
        计算文件的sha1值
        :param file_b64:
        :param hexadecimal:
        :param b64:
        :return:
        """
        from utils.encodes import hash_code

        sha1 = hashlib.sha1()
        sha1.update(base64.b64decode(file_b64))
        return hash_code(sha1, hexadecimal, b64)

    @staticmethod
    def get_md5_b64(file_b64, hexadecimal=True, b64=False):
        """
        计算文件的md5值
        :param file_b64:
        :param hexadecimal:
        :param b64:
        :return:
        """
        from utils.encodes import hash_code

        md5 = hashlib.md5()
        md5.update(base64.b64decode(file_b64))
        return hash_code(md5, hexadecimal, b64)

    @classmethod
    def base64_to_pdf(cls, base64_str, file_dir, file_name):
        """
        base64 转 pdf
        :param base64_str:
        :param file_dir:
        :param file_name:
        :return:
        """
        from utils.encodes import base64_to_file
        return base64_to_file(base64_str, file_dir, file_name, FileFormat.PDF.value)

    @classmethod
    def base64_to_jpg(cls, base64_str, file_dir, file_name):
        """
        base64 转 JPG
        :param base64_str:
        :param file_dir:
        :param file_name:
        :return:
        """
        from utils.encodes import base64_to_file
        base64_to_file(base64_str, file_dir, file_name, FileFormat.JPG.value)

    @classmethod
    def base64_to_png(cls, base64_str, file_dir, file_name):
        """
        base64 转 PNG
        :param base64_str:
        :param file_dir:
        :param file_name:
        :return:
        """
        from utils.encodes import base64_to_file
        base64_to_file(base64_str, file_dir, file_name, FileFormat.PNG.value)

    @staticmethod
    def creat_dirs(dir_path):
        """
        创建多级目录
        :param dir_path:
        :return:
        """
        Assert.is_true(dir_path, '目录不能为空')
        dir_path = dir_path.strip()
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        Assert.is_true(os.path.isdir(dir_path), '创建目录失败：{0}'.format(dir_path))
        return dir_path

    @staticmethod
    def get_path_name_ext(file_path):
        """
        解析文件路径，文件名，文件扩展
        :param file_path:
        :return:
        """
        Assert.is_true(os.path.isfile(file_path), '文件不存在, path: {0}'.format(file_path))
        (path, file_name) = os.path.split(file_path)
        (name, ext) = os.path.splitext(file_name)
        return path, name, ext.strip(os.curdir)

    @staticmethod
    def get_file_size(file_path):
        """
        获取文件大小 保留两位小数，单位MB
        :param file_path:
        :return:
        """
        Assert.is_true(os.path.isfile(file_path), '文件不存在, path: {0}'.format(file_path))
        return round(os.path.getsize(file_path) / float(1024 * 1024), 2)

    @staticmethod
    def get_file_access_time(file_path):
        """
        获取文件访问时间
        :param file_path:
        :return:
        """
        Assert.is_true(os.path.isfile(file_path), '文件不存在, path: {0}'.format(file_path))
        return os.path.getatime(file_path)

    @staticmethod
    def get_file_create_time(file_path):
        """
        获取文件创建时间
        :param file_path:
        :return:
        """
        Assert.is_true(os.path.isfile(file_path), '文件不存在, path: {0}'.format(file_path))
        return os.path.getctime(file_path)

    @staticmethod
    def get_file_modify_time(file_path):
        """
        获取文件修改时间
        :param file_path:
        :return:
        """
        if not os.path.isfile(file_path):
            raise MyError(code=requests.codes.server_error, msg='文件不存在, path: {0}'.format(file_path))
        return os.path.getatime(filename=file_path)

    @staticmethod
    def get_files_by_suffix(dir, suffixs):
        """
        获取目录下包括子目录所有符合后缀条件的文件路径列表
        :param dir: 目录
        :param suffixs: 后缀
        :return:
        """
        if not os.path.isdir(dir) or not os.path.exists(dir):
            raise MyError(code=requests.codes.server_error, msg='不是有效的路径, path: {0}'.format(dir))
        file_list = []
        sub_dirs = [x[0] for x in os.walk(top=dir)]
        # sub_dirs.remove(dir)

        # 读取所有子目录
        for sub_dir in sub_dirs:
            for suffix in suffixs:
                file_glob = os.path.join(sub_dir, '*.' + suffix)
                # glob.glob() 返回所有匹配的文件路径列表
                # extend() 函数用于在列表末尾一次性追加另一个序列中的多个值
                file_list.extend(glob.glob(pathname=file_glob))
        return file_list

    @staticmethod
    def get_files_by_suffix2(dir, suffixs):
        """
        获取目录下所有符合后缀条件的文件路径列表
        :param dir:目录
        :param suffixs:后缀
        :return:
        """
        Assert.is_true(assert_condition=os.path.isdir(dir), assert_msg='路径无效：{0}'.format(dir))
        file_list = []
        for suffix in suffixs:
            file_glob = os.path.join(dir, '*.' + suffix)
            file_list.extend(glob.glob(pathname=file_glob))
        return file_list

    @classmethod
    def copy_file(cls, old_file, new_file):
        """
        复制文件到指定目录
        :param old_file:源文件路径
        :param new_file:新文件目录
        :return:
        """
        Assert.is_true(os.path.isfile(old_file), '文件不存在：{0}'.format(old_file))
        file_name = os.path.basename(old_file)
        FileUtil.creat_dirs(new_file)
        new_file_path = os.path.join(new_file, file_name)
        shutil.copyfile(src=old_file, dst=new_file_path)
        return cls.normcase(new_file_path)

    @staticmethod
    def del_dir(dir_path):
        """
        删除文件夹及内容
        :param dir_path:
        :return:
        """
        import shutil
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def del_file(file_path):
        """
        删除文件
        :param file_path:
        :return:
        """
        Assert.is_true(os.path.isfile(file_path), '文件不存在：{0}'.format(file_path))
        os.remove(file_path)

    @classmethod
    def rename(cls, file_path, file_name):
        """
        文件重命名
        :param file_path: 源文件路径
        :param file_name: 新文件名
        :return:
        """
        path, name, ext = cls.get_path_name_ext(file_path)
        os.rename(file_path, cls.path_join(path, file_name + _curdir + ext))

    @classmethod
    def path_join(cls, path, *paths):
        """
        路径拼接
        :param path:
        :param paths:
        :return:
        """
        return cls.normcase(os.path.join(path, *paths))

    @staticmethod
    def normcase(path):
        """
        规范化路径格式, 所有反斜杠变为斜杠
        :param str path:
        :return:
        """
        return path.replace(_sep, _altsep)


@unique
class FileFormat(Enum):
    """
    文件扩展
    """
    PNG = 'PNG'
    JPG = 'JPG'
    PDF = 'PDF'


if __name__ == '__main__':
    # from utils.encodes import file_to_base64
    # base_str = file_to_base64('D:/AIData/1.pdf')
    # print(FileUtil.get_md5_b64(base_str))

    # print(FileUtil.get_path_name_ext('D:/AIData/1.pdf'))

    FileUtil.rename('D:/AIData/1.pdf', '测试')



