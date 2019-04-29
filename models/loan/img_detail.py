#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 贷款图片文件明细
# @Author : Zackeus
# @File : img_detail.py 
# @Software: PyCharm
# @Time : 2019/4/2 14:45


import os
from extensions import db
from models.basic import BasicModel, BaseSchema
from models.loan.img_type import ImgTypeSchema
from utils import validates as MyValidates
from marshmallow import fields, validate


class ImgDetailModel(BasicModel):
    """
    贷款图片明细
    """

    __tablename__ = 'LOAN_IMG_DETAIL'

    loan_file_id = db.Column(
        db.String(length=64),
        db.ForeignKey('LOAN_FILE.ID'),
        name='LOAN_FILE_ID',
        nullable=False,
        index=True
    )

    parent_file_id = db.Column(
        db.String(length=64),
        name='PARENT_FILE_ID',
        nullable=False,
        index=True,
        comment='父级文件ID'
    )

    file_id = db.Column(db.String(length=64), name='FILE_ID', nullable=False, unique=True, index=True, comment='图片ID')

    img_type_id = db.Column(
        db.String(length=64),
        db.ForeignKey('LOAN_IMG_TYPE.ID'),
        name='IMG_TYPE_ID',
        index=True
    )

    is_handle = db.Column(db.Boolean, name='IS_HANDLE', nullable=False, default=False, comment='是否分类处理')
    err_code = db.Column(db.String, name='ERR_CODE', comment='错误代号')
    err_msg = db.Column(db.String(length=100), name='ERR_MSG', comment='错误信息')

    @property
    def file_data(self):
        """
        文件的base64字符
        :return:
        """
        from models.file import FileModel
        from utils.encodes import file_to_base64
        file_model = FileModel().dao_get(self.file_id)  # type: FileModel
        file_path = file_model.file_path
        return file_to_base64(file_path) if os.path.isfile(file_path) else None

    img_type = db.relationship(
        argument='ImgTypeModel',
        back_populates='img_details'
    )

    loan_file = db.relationship(
        argument='LoanFileModel',
        back_populates='img_details'
    )

    def dao_add(self, loan_file_id, parent_file_id, file_id, **kwargs):
        """
        图片明细入库
        :param loan_file_id: 贷款文件入库流水号
        :param parent_file_id: 父级文件ID
        :param file_id: 图片文件ID
        :param kwargs:
        :return:
        """
        super().dao_create()
        self.loan_file_id = loan_file_id
        self.parent_file_id = parent_file_id
        self.file_id = file_id
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)

    def dao_get_todo_by_loan_file(self, loan_file):
        """
        查询待处理贷款流程明细
        :param loan_file: 贷款流水模型
        :return:
        """
        return self.query.filter(ImgDetailModel.loan_file_id == loan_file.id, ImgDetailModel.is_handle == False).all()


class ImgDetailSchema(BaseSchema):
    """
    贷款图片明细
    """
    __model__ = ImgDetailModel

    loan_file_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='loanFileId'
    )

    parent_file_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='parentFileId'
    )

    file_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='fileId'
    )

    img_type_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='imgTypeId'
    )

    is_handle = fields.Boolean(load_from='isHandle')

    err_code = fields.Str()
    err_msg = fields.Str(validate=validate.Length(max=100))
    file_data = fields.Str(required=True, dump_only=True)

    img_type = fields.Nested(
        ImgTypeSchema,
        only=('type_code', 'type_explain'),
        load_from='imgType'
    )
