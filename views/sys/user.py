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


@user_bp.route('/login/<string:login_name>')
def login(login_name):
    """

    :param login_name:
    :return:
    """
    import hashlib

    user = User().dao_get_by_login_name(login_name)  # type: User
    password = user.password
    print(password)

    salt = bytes.fromhex(password[0:16])

    sha1 = hashlib.sha1(salt)
    sha1.update(bytes('a1!', encoding='utf8'))
    res = sha1.digest()

    for i in range(1, 1024):
        res = hashlib.sha1(res).digest()
    print(salt.hex() + res.hex())
    return 'OK'

