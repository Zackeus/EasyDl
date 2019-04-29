#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : loan_type.py 
# @Software: PyCharm
# @Time : 2019/3/29 16:44


from marshmallow import fields

from extensions import db, cache
from models.basic import BasicModel, BaseSchema
from utils import validates


class LoanTypeModel(BasicModel):
    """
    贷款类型
    """
    __tablename__ = 'LOAN_TYPE'

    loan_type_name = db.Column(
        db.String(length=10),
        name='LOAN_TYPE_NAME',
        index=True,
        unique=True,
        nullable=False,
        comment='贷款类型'
    )
    loan_dir = db.Column(
        db.String(length=20),
        name='LOAN_DIR',
        index=True,
        unique=True,
        nullable=False,
        comment='贷款目录名'
    )

    loan_files = db.relationship(
        argument='LoanFileModel',
        back_populates='loan_type',
        cascade='all'
    )

    def dao_add(self, subtransactions=False, nested=False):
        super().dao_create()
        with db.auto_commit_db(subtransactions=subtransactions, nested=nested) as s:
            s.add(self)

    @cache.memoize()
    def dao_get_by_type(self, type_name):
        """
        根据类型字符查询
        :param type_name:
        :return:
        """
        return self.query.filter_by(loan_type_name=type_name).first()


class LoanTypeSchema(BaseSchema):
    """
    贷款类型校验器
    """
    __model__ = LoanTypeModel

    loan_type_name = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=10, not_empty=False),
        load_from='loanTypeName'
    )

    loan_dir = fields.Str(
        required=True,
        validate=validates.MyLength(min=1, max=20, not_empty=False),
        load_from='loanDir'
    )

    def only_create(self):
        return super().only_create() + ('loan_type_name', 'loan_dir')




