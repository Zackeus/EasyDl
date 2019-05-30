#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : lexer.py 
# @Software: PyCharm
# @Time : 2019/5/30 8:46


from marshmallow import fields

from extensions import db, cache
from models.basic import BasicModel, BaseSchema
from utils import validates as MyValidates


class AudioLexerModel(BasicModel):
    """
    词性分析
    """
    __tablename__ = 'AUDIO_LEXER'
    default_title = '未定义'
    default_color = '#000099'

    code = db.Column(db.String(length=64), name='CODE', nullable=False, index=True, unique=True, comment='词性code')
    title = db.Column(db.String(length=60), name='TITLE', nullable=False, default=default_title, comment='词性说明')
    color = db.Column(db.String(length=30), name='COLOR', nullable=False, default=default_color, comment='词性颜色')

    def dao_create(self, id=None, **kwargs):
        super().dao_create(id)
        with db.auto_commit_db(**kwargs) as s:
            s.add(self)

    def dao_get_by_codes(self, codes):
        """
        根据code列表查询数据
        :param list codes:
        :return:
        """
        audio_lexers = []
        # 列表去重查询
        for code in list(set(codes)):
            audio_lexers.append(self.dao_get_by_code(code))
        return audio_lexers

    @cache.memoize()
    def dao_get_by_code(self, code):
        """
        根据code查询数据
        :param str code:
        :return:
        """
        return self.query.filter_by(code=code).first()


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
