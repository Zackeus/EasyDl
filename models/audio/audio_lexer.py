#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : lexer.py 
# @Software: PyCharm
# @Time : 2019/5/30 8:46


from marshmallow import fields

from extensions import db
from models.basic import BasicModel, BaseSchema
from utils import validates as MyValidates


class AudioLexerModel(BasicModel):
    """
    词性分析
    """
    __tablename__ = 'AUDIO_LEXER'

    code = db.Column(db.String(length=64), name='CODE', nullable=False, index=True, unique=True, comment='词性code')
    title = db.Column(db.String(length=60), name='TITLE', nullable=False, default='未定义', comment='词性说明')
    color = db.Column(db.String(length=30), name='COLOR', nullable=False, default='#000099', comment='词性颜色')


class AudioLexerSchema(BaseSchema):
    """
    词性分析校验器
    """
    __model__ = AudioLexerModel

    code = fields.Str(required=True, validate=MyValidates.MyLength(min=1, max=64, not_empty=False))
    title = fields.Str(required=True, validate=MyValidates.MyLength(min=1, max=60, not_empty=False))
    color = fields.Str(required=True, validate=MyValidates.MyLength(min=1, max=30, not_empty=False))

    def only_create(self):
        return super().only_create() + ('code', 'title', 'color')
