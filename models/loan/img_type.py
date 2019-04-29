#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 贷款图片文件类型
# @Author : Zackeus
# @File : img_type.py 
# @Software: PyCharm
# @Time : 2019/4/2 13:37


from extensions import db, cache
from models.basic import BasicModel, BaseSchema
from marshmallow import fields
from utils import validates


class ImgTypeModel(BasicModel):
    """
    图片类型
    """

    __tablename__ = 'LOAN_IMG_TYPE'

    type_code = db.Column(
        db.String(length=10),
        name='TYPE_CODE',
        index=True,
        unique=True,
        nullable=False,
        comment='类型代号'
    )

    type_explain = db.Column(db.String(length=20), name='TYPE_EXPLAIN', nullable=False, comment='类型说明')
    is_ocr = db.Column(db.Boolean, name='IS_OCR', nullable=False, default=False, comment='是否需要OCR识别')

    img_details = db.relationship(
        argument='ImgDetailModel',
        back_populates='img_type',
        cascade='all'
    )

    def dao_add(self, **kwargs):
        super().dao_create()
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)

    @cache.memoize()
    def dao_get_by_code(self, type_code):
        """
        根据类型 code 查询
        :param type_code:
        :return:
        """
        return self.query.filter_by(type_code=type_code).first()


class ImgTypeSchema(BaseSchema):
    """
    图片类型校验
    """
    __model__ = ImgTypeModel

    type_code = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=10, not_empty=False),
        load_from='typeCode'
    )

    type_explain = fields.Str(required=True, validate=validates.Length(min=1, max=20), load_from='typeExplain')
    is_ocr = fields.Boolean(required=True, load_from='isOcr')

    def only_create(self):
        return super().only_create() + ('type_code', 'type_explain', 'is_ocr')



