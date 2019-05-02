#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : user.py 
# @Software: PyCharm
# @Time : 2019/4/16 14:08


from flask import Blueprint

from models.sys.user import User


user_bp = Blueprint('user', __name__)


@user_bp.route('/login/<string:login_name>/<string:password>')
def login(login_name, password):
    """

    :param password:
    :param login_name:
    :return:
    """
    user = User().dao_get_by_login_name(login_name)  # type: User
    print(user.validate_password(password))
    return 'OK'

