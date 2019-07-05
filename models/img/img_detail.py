#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 图片文件明细
# @Author : Zackeus
# @File : img_detail.py 
# @Software: PyCharm
# @Time : 2019/4/2 14:45


import os
from extensions import db
from models.basic import BasicModel, BaseSchema
from models.img.img_type import ImgTypeSchema
from utils import validates as MyValidates, is_not_empty
from marshmallow import fields, validate


class ImgDetailModel(BasicModel):
    """
    图片明细
    """

    __tablename__ = 'IMG_DETAIL'

    img_data_id = db.Column(
        db.String(length=64),
        db.ForeignKey('IMG_DATA.ID'),
        name='IMG_DATA_ID',
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
        db.ForeignKey('IMG_TYPE.ID'),
        name='IMG_TYPE_ID',
        index=True
    )

    is_handle = db.Column(db.Boolean, name='IS_HANDLE', nullable=False, default=False, comment='是否分类处理')
    err_code = db.Column(db.String, name='ERR_CODE', comment='错误代号')
    err_msg = db.Column(db.String(length=100), name='ERR_MSG', comment='错误信息')

    @property
    def file_md5(self):
        """
        图片文件md5值
        :return:
        """
        from models.file import FileModel
        file_model = FileModel().dao_get(self.file_id)  # type: FileModel
        return file_model.md5_id if is_not_empty(file_model) else None

    @property
    def file_data(self):
        """
        图片文件的base64字符
        :return:
        """
        from models.file import FileModel
        from utils.encodes import file_to_base64
        file_model = FileModel().dao_get(self.file_id)  # type: FileModel
        file_path = file_model.file_path
        return file_to_base64(file_path) if os.path.isfile(file_path) else None

    @property
    def file_path(self):
        """
        图片文件路径
        :return:
        """
        from models.file import FileModel
        file_model = FileModel().dao_get(self.file_id)  # type: FileModel
        return file_model.file_path if is_not_empty(file_model) else None

    img_data = db.relationship(
        argument='ImgDataModel',
        back_populates='img_details'
    )

    img_type = db.relationship(
        argument='ImgTypeModel',
        back_populates='img_details'
    )

    def __init__(self, img_type_code=None, **kwargs):
        """

        :param str img_type_code: 图片类型
        :param kwargs:
        """
        super(self.__class__, self).__init__(**kwargs)
        self.img_type_code = img_type_code

    def dao_add(self, img_data_id, parent_file_id, file_id, **kwargs):
        """
        图片明细入库
        :param img_data_id: 图片文件入库流水号
        :param parent_file_id: 父级文件ID
        :param file_id: 图片文件ID
        :param kwargs:
        :return:
        """
        super().dao_create()
        self.img_data_id = img_data_id
        self.parent_file_id = parent_file_id
        self.file_id = file_id
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)

    def dao_get_todo_by_img_data(self, img_data):
        """
        查询待处理图片明细
        :param img_data: 图片流水模型
        :return:
        """
        return self.query.filter(ImgDetailModel.img_data_id == img_data.id, ImgDetailModel.is_handle == False).all()

    def dao_get_children(self, parent_file_id):
        """
        根据父级ID查询子集
        :param parent_file_id:
        :return:
        """
        return self.query.filter(ImgDetailModel.parent_file_id == parent_file_id).all()

    def dao_update_type(self, type_id):
        """
        更新图片文件类型
        :param type_id:
        :return:
        """
        self.img_type_id = type_id
        super().dao_update()


class ImgDetailSchema(BaseSchema):
    """
    图片资料明细
    """
    __model__ = ImgDetailModel

    img_data_id = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=64, not_empty=False),
        load_from='imgDataId'
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
    file_path = fields.Str(required=True, dump_only=True)
    file_md5 = fields.Str(required=True, dump_only=True)
    img_type_code = fields.Str(
        required=True,
        validate=MyValidates.MyLength(min=1, max=10, not_empty=False),
        load_only=True,
        load_from='imgTypeCode'
    )

    img_type = fields.Nested(
        ImgTypeSchema,
        only=('type_code', 'type_explain'),
        load_from='imgType'
    )

    def only_patch_type(self):
        return super().only_update() + ('id', 'img_type_code', )

    def dump_only_page(self):
        return super().dump_only_page() + \
               ('img_data_id', 'parent_file_id', 'file_id', 'img_type_id', 'is_handle', 'err_code', 'err_msg',
                'img_type', 'file_md5', )