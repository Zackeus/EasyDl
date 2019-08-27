#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : ocr_file.py 
# @Software: PyCharm
# @Time : 2019/8/27 11:45

import os
from extensions import db

from models.basic import BasicModel, BaseSchema
from models.file import FileSchema
from models.sys import SysDict

from utils import validates as MyValidates, is_not_empty
from utils.file import FileFormat
from marshmallow import fields, validates, ValidationError


class OcrFile(BasicModel):
    """
    OCR 识别模型
    """
    __tablename__ = 'OCR_FILE'

    __table_args__ = (
        db.Index('ix_{0}_APP_ID_APP_SYS_ID'.format(__tablename__), 'APP_ID', 'APP_SYS_ID', unique=True),
    )

    app_id = db.Column(db.String(length=64), name='APP_ID', nullable=False, comment='应用ID')
    app_sys_id = db.Column(
        db.String(length=64),
        db.ForeignKey('SYS_DICT.ID'),
        name='APP_SYS_ID',
        nullable=False,
        index=True
    )

    file_id = db.Column(db.String(length=64), name='FILE_ID', nullable=False, unique=True, index=True, comment='文件ID')

    @property
    def app_sys_code(self):
        """
        应用系统代号
        :return:
        """
        if self.app_sys_id:
            app_sys = SysDict().dao_get(self.app_sys_id)
            return app_sys.value if is_not_empty(app_sys) else '查无此来源系统.'
        elif self._app_sys_code:
            return self._app_sys_code
        return None

    def __init__(self, file_data=None, app_sys_code=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.file_data = file_data
        self._app_sys_code = app_sys_code

    def dao_add(self, **kwargs):
        super().dao_create()
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)


class OcrFileSchema(BaseSchema):
    """
    OCR模型校验
    """
    __model__ = OcrFile
    __file_formats = (FileFormat.JPEG.value, FileFormat.JPG.value, FileFormat.PNG.value)

    app_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='appId'
    )

    app_sys_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='appSysId'
    )

    app_sys_code = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='appSysCode'
    )

    file_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='fileId'
    )

    file_data = fields.Nested(
        FileSchema,
        required=True,
        load_only=True,
        load_from='fileData'
    )

    @validates('file_data')
    def validate_file_data(self, value):
        """
        文件校验
        :param value:
        :return:
        """
        if isinstance(value, dict):
            # 前面校验失败会返回dict而不是对象
            pass
        else:
            if value.file_name.find(os.curdir) != -1:
                raise ValidationError('文件名包含特殊字符')
            if value.file_format.upper() not in self.__file_formats:
                raise ValidationError('无效的文件格式')

    def only_create(self):
        return super().only_create() + \
               ('app_id', 'app_sys_code', 'file_data.file_name', 'file_data.file_format', 'file_data.file_base64')
