#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : user.py 
# @Software: PyCharm
# @Time : 2019/4/16 14:08


from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_user, logout_user

from utils import Method, ContentType, codes, validated, render_info, MyResponse, redirect_back, \
    is_not_empty, Assert
from models.sys.user import User, UserSchema


user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=[Method.GET.value])
def login():
    if current_user.is_authenticated:
        # 用户已登录认证
        return redirect(location=url_for(endpoint='sys.index'))
    return render_info(MyResponse(msg='账号未登录!', code=codes.not_logged_in), template='sys/login.html')


@user_bp.route('/login', methods=[Method.POST.value])
@validated(UserSchema, only=UserSchema().only_login(), consumes=ContentType.JSON.value)
def login_validate(user):
    """
    登录验证
    :param user:
    :return:
    """
    if current_user.is_authenticated:
        return render_info(MyResponse(msg='登录成功'))

    real_user = User().dao_get_by_login_name(user.login_name)  # type: User
    Assert.is_true(is_not_empty(real_user), assert_code=codes.login_fail, assert_msg='账号未注册')
    if real_user.validate_password(user.password):
        # 密码验证成功
        login_user(real_user, False)
        return render_info(MyResponse(msg='登录成功'))
    return render_info(MyResponse(code=codes.login_fail, msg='用户名或密码不正确'))


@user_bp.route('/logout', methods=[Method.GET.value])
def logout():
    """
    用户登出
    :return:
    """
    logout_user()
    return redirect_back()


