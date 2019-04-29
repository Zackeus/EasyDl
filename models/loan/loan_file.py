#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : loan_file.py 
# @Software: PyCharm
# @Time : 2019/3/26 14:31

import os
from flask import current_app
from extensions import db

from models.basic import BasicModel, BaseSchema
from models.file import FileModel, FileSchema
from models.loan.loan_type import LoanTypeModel, LoanTypeSchema
from models.loan.flow_type import FlowTypeModel, FlowTypeSchema
from models.loan.img_detail import ImgDetailModel, ImgDetailSchema
from utils.encodes import base64_to_file
from utils.file.file import FileUtil, FileFormat
from utils.file.pdf import PDFUtil
from utils.object_util import is_not_empty, is_empty
from utils import validates as MyValidates
from marshmallow import fields, validate, validates, ValidationError


class LoanFileModel(BasicModel):
    """
    贷款文件
    """
    __tablename__ = 'LOAN_FILE'

    loan_type_id = db.Column(
        db.String(length=64),
        db.ForeignKey('LOAN_TYPE.ID'),
        name='LOAN_TYPE_ID',
        nullable=False,
        index=True
    )

    flow_type_id = db.Column(
        db.String(length=64),
        db.ForeignKey('FLOW_TYPE.ID'),
        name='FLOW_TYPE_ID',
        nullable=False,
        index=True
    )

    application_num = db.Column(db.String(length=64), name='APPLICATION_NUM', index=True, comment='申请号')
    contract_num = db.Column(db.String(length=64), name='CONTRACT_NUM', index=True, comment='合同号')
    name = db.Column(db.String(length=100), name='NAME', nullable=False, comment='姓名')
    id_card = db.Column(db.String(length=32), name='ID_CARD', nullable=False, comment='身份证号')
    agent = db.Column(db.String(length=100), name='AGENT', comment='经销商')
    title = db.Column(db.String(length=50), name='TITLE', comment='邮件标题')
    content = db.Column(db.Text, name='CONTENT', comment='邮件正文')
    page_num = db.Column(db.Integer, name='PAGE_NUM', nullable=False, default=0, comment='PDF总页码数')
    success_num = db.Column(db.Integer, name='SUCCESS_NUM', nullable=False, default=0, comment='图片分割成功数')
    fail_num = db.Column(db.Integer, name='FAIL_NUM', nullable=False, default=0, comment='图片分割失败数')
    is_handle = db.Column(db.Boolean, name='IS_HANDLE', nullable=False, default=False, comment='是否处理完')
    push_url = db.Column(db.String, name='PUSH_URL', comment='推送地址')
    push_times = db.Column(db.Integer, name='PUSH_TIMES', nullable=False, default=0, comment='推送次数')
    is_push = db.Column(db.Boolean, name='IS_PUSH', nullable=False, default=False, comment='是否成功推送')

    loan_type = db.relationship(
        argument='LoanTypeModel',
        back_populates='loan_files'
    )

    flow_type = db.relationship(
        argument='FlowTypeModel',
        back_populates='loan_files'
    )

    img_details = db.relationship(
        argument='ImgDetailModel',
        back_populates='loan_file',
        cascade='all'
    )

    def __init__(self, file_data=None, **kwargs):
        """

        :param file_data:
        :param kwargs:
        """
        super(LoanFileModel, self).__init__(**kwargs)
        self.file_data = file_data

    def dao_add_info(self, loan_dir, subtransactions=False, nested=False):
        """
        信息入库
        :param nested:
        :param subtransactions:
        :param loan_dir: 资料目录
        :return:
        """
        with db.auto_commit_db(subtransactions, nested, error_call=FileUtil.del_dir, dir_path=loan_dir) as s:
            s.add(self)

            # 写入磁盘
            file_models = []
            for file in self.file_data:
                file_path = base64_to_file(file.file_base64, loan_dir, file.file_name, file.file_format)

                # 文件入库
                file_model = FileModel()
                file_model.dao_init_file(file_path, nested=True)

                file_models.append(file_model)

            # 图片处理明细信息
            details = []
            for file_model in file_models:
                if file_model.file_format.strip().upper() == FileFormat.PDF.value:
                    # 文件为pdf, 分割 pdf, 更新资料信息
                    img_path = FileUtil.path_join(loan_dir, current_app.config.get('LOAN_DIR_IMG'), file_model.id)
                    page_num, img_num, fail_num, detail_info = PDFUtil.pdf_to_pic(file_model.file_path, img_path)

                    images = detail_info.get('images', None)
                    if img_num > 0 and is_not_empty(images):
                        for image in images:
                            if is_empty(image.get('error_msg', None)):
                                # 图片文件入库
                                img_model = FileModel()
                                img_model.dao_init_file(image.get('img_path', ''), nested=True)
                                # 图片明细入库
                                img_detail = ImgDetailModel()
                                img_detail.dao_add(self.id, file_model.id, img_model.id, nested=True)

                    self.page_num += page_num
                    self.success_num += img_num
                    self.fail_num += fail_num
                    details.append(dict(id=file_model.id, md5=file_model.md5_id,
                                        page_num=page_num, success_num=img_num, fail_num=fail_num))
                else:
                    # 文件备份， 迁移处理文件
                    new_img_path = FileUtil.copy_file(
                        file_model.file_path,
                        FileUtil.path_join(loan_dir, current_app.config.get('LOAN_DIR_IMG')))

                    # 图片文件入库
                    img_model = FileModel()
                    img_model.dao_init_file(new_img_path, nested=True)
                    # 文件为图片, 图片明细入库
                    img_detail = ImgDetailModel()
                    img_detail.dao_add(self.id, file_model.id, img_model.id, nested=True)

                    self.page_num += 1
                    self.success_num += 1
                    self.fail_num += 0
                    details.append(dict(id=file_model.id, md5=file_model.md5_id, page_num=1, success_num=1, fail_num=0))
        return dict(id=self.id, details=details)

    def dao_get_todo(self, type_name, limit=10):
        """
        根据贷款类型查询待处理数据
        :param type_name: 贷款类型
        :param limit:
        :return:
        """
        return self.query.join(LoanTypeModel, LoanFileModel.loan_type_id == LoanTypeModel.id). \
            filter(LoanTypeModel.loan_type_name == type_name, LoanFileModel.is_handle == False). \
            order_by(LoanFileModel.create_date.asc()).limit(limit).all()

    def dao_get_push(self):
        """
        查询待推送数据
        :return:
        """
        return self.query.filter(LoanFileModel.is_handle == True,
                                 LoanFileModel.is_push == False,
                                 LoanFileModel.push_times < 5).\
            order_by(LoanFileModel.create_date.asc()).all()


class LoanFileSchema(BaseSchema):
    """
    贷前文件校验器
    """
    __model__ = LoanFileModel
    __file_formats = (FileFormat.PDF.value, FileFormat.JPG.value, FileFormat.PNG.value)

    application_num = fields.Str(validate=validate.Length(max=64), load_from='applicationNum')
    contract_num = fields.Str(validate=validate.Length(max=64), load_from='contractNum')
    name = fields.Str(required=True, validate=MyValidates.MyLength(min=1, max=100, not_empty=False))
    id_card = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=18, max=32, not_empty=False),
        load_from='idCard'
    )
    agent = fields.Str(validate=validate.Length(max=100))
    title = fields.Str(validate=validate.Length(max=50))
    content = fields.Str()
    page_num = fields.Integer(load_from='pageNum')
    success_num = fields.Integer(load_from='successNum')
    fail_num = fields.Integer(load_from='failNum')
    is_handle = fields.Boolean(load_only=True, load_from='isHandle')
    push_url = fields.Str(load_only=True, validate=validate.URL(), load_from='pushUrl')
    push_times = fields.Integer(load_only=True, load_from='pushTimes')
    is_push = fields.Boolean(load_only=True, load_from='isPush')

    file_data = fields.Nested(
        FileSchema,
        required=True,
        many=True,
        load_only=True,
        load_from='fileData'
    )

    loan_type = fields.Nested(
        LoanTypeSchema,
        only=('id', 'loan_type_name', 'loan_dir'),
        required=True,
        load_from='loanType'
    )

    flow_type = fields.Nested(
        FlowTypeSchema,
        only=('id', 'flow_type_name', 'flow_dir'),
        required=True,
        load_from='flowType'
    )

    img_details = fields.Nested(
        ImgDetailSchema,
        many=True,
        only=('id', 'parent_file_id', 'file_id', 'err_code', 'err_msg', 'file_data', 'img_type'),
        load_from='imgDetails'
    )

    @validates('file_data')
    def validate_pdf_name(self, values):
        """
        文件校验
        :param values:
        :return:
        """
        for value in values:
            if value.file_name.find(os.curdir) != -1:
                raise ValidationError('文件名包含特殊字符')
            if value.file_format.upper() not in self.__file_formats:
                raise ValidationError('无效的文件格式')

    @validates('loan_type')
    def validate_loan_type(self, value):
        """
        校验贷款类型
        :type value: LoanFileModel
        """
        type_name = value.loan_type_name
        loan_type = LoanTypeModel().dao_get_by_type(type_name)
        if is_empty(loan_type):
            raise ValidationError('无效的贷款类型.')

    @validates('flow_type')
    def validate_flow_type(self, value):
        """
        校验流程类型
        :type value: FlowTypeModel
        """
        type_name = value.flow_type_name
        flow_type = FlowTypeModel().dao_get_by_type(type_name)
        if is_empty(flow_type):
            raise ValidationError('无效的流程类型.')

    def only_create(self):
        return super().only_create() + \
               ('loan_type.loan_type_name', 'flow_type.flow_type_name',
                'file_data.file_name', 'file_data.file_format', 'file_data.file_base64',
                'application_num', 'contract_num', 'name', 'id_card', 'agent', 'title', 'content', 'push_url')












