#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : file.py 
# @Software: PyCharm
# @Time : 2019/3/26 14:11


from flask import current_app
from extensions import db
from models.basic import BasicModel, BaseSchema

from utils.file.file import FileUtil
from utils.encodes import AESUtil
from utils import validates
from marshmallow import fields


class FileModel(BasicModel):
    """
    文件模型
    """
    __tablename__ = 'FILE'

    md5_id = db.Column(db.String(length=64), name='MD5_ID', index=True, nullable=False, comment='文件MD5值')
    file_name = db.Column(db.String(length=64), name='FILE_NAME', nullable=False, comment='文件名')
    file_format = db.Column(db.String(length=20), name='FILE_FORMAT', nullable=False, comment='文件格式')
    file_size = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=False),
        name='FILE_SIZE',
        nullable=False,
        default=0.00,
        comment='文件大小'
    )
    file_path_hash = db.Column(db.String, name='FILE_PATH_HASH', nullable=False, comment='文件路径密文')

    @property
    def file_path(self):
        aes = AESUtil(current_app.config.get('DATA_PATH_KEY'))
        return aes.decrypt(self.file_path_hash)

    @file_path.setter
    def file_path(self, file_path):
        """
        设置路径
        :param file_path:
        :return:
        """
        # 文件路径加密
        aes = AESUtil(current_app.config.get('DATA_PATH_KEY'))
        self.file_path_hash = aes.encrypt(file_path)

    def __init__(self, file_base64=None, **kwargs):
        super(FileModel, self).__init__(**kwargs)
        self.file_base64 = file_base64

    def dao_init_file(self, file_path, id=None, subtransactions=False, nested=False):
        """
        根据路径解析入库
        :param nested:
        :param subtransactions:
        :param file_path: 文件路径
        :param id:
        :return:
        """
        with db.auto_commit_db(subtransactions=subtransactions, nested=nested) as s:
            super().dao_create(id)
            # 计算文件 md5
            self.md5_id = FileUtil.get_md5_path(file_path)
            # noinspection PyAttributeOutsideInit
            self.file_path = file_path
            _, self.file_name, self.file_format = FileUtil.get_path_name_ext(file_path)
            self.file_size = FileUtil.get_file_size(file_path)
            s.add(self)


class FileSchema(BaseSchema):
    """
    文件校验器
    """
    __model__ = FileModel

    file_name = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=64, not_empty=False),
        load_from='fileName'
    )
    file_format = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=20, not_empty=False),
        load_from='fileFormat'
    )
    # file_path = fields.Str(required=True, validate=validates.MyLength(min=1, not_empty=False), load_from='filePath')
    file_size = fields.Decimal(places=2, required=True, load_from='fileSize')
    file_base64 = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, not_empty=False),
        load_from='fileBase64'
    )







