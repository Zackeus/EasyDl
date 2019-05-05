#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 扩展实例化
# @Author : Zackeus
# @File : extensions.py 
# @Software: PyCharm
# @Time : 2019/3/21 10:23


import os
import logging
import time
from functools import wraps
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate
from flask_apscheduler import APScheduler as BaseAPScheduler
from apscheduler.events import JobExecutionEvent, EVENT_JOB_ERROR
from flask_caching import Cache as BaseCache
from flask_wtf import CSRFProtect as BaseCSRFProtect
from flask_login import LoginManager, AnonymousUserMixin
from flask_session import Session


from utils.file.file import FileUtil
from utils.assert_util import Assert
from utils.object_util import is_not_empty
from utils.encodes import Unicode
from utils.response import MyResponse
from utils.msg import WXMsg


class SQLAlchemy(BaseSQLAlchemy):

    @contextmanager
    def auto_commit_db(self, subtransactions=False, nested=False, error_call=None, **kwargs):
        """
        利用contextmanager管理器,对try/except语句封装，使用的时候必须和with结合
        :param nested: 是否嵌套
        :param error_call: 异常回调函数
        :param subtransactions: 是否子事务
        :return:
        """
        try:
            if subtransactions or nested:
                self.session.begin(subtransactions=subtransactions, nested=nested)
            yield self.session
            self.session.commit()
        except Exception as e:
            # 加入数据库commit提交失败，必须回滚！！！
            self.session.rollback()
            if error_call:
                error_call(**kwargs)
            raise e


class APScheduler(BaseAPScheduler):

    _ERROR_MSG = '【裕隆汽车金融】定时任务异常【{job_id}】：{msg}'

    def init_app(self, app):
        super().init_app(app)
        self.add_listener(self.error_listener, EVENT_JOB_ERROR)

    def error_listener(self, event):
        """
        定时异常监听
        :type event: JobExecutionEvent
        :param event: 
        :return: 
        """
        res = MyResponse.init_error(event.exception)
        try:
            self.app.logger.exception(event.exception)
        finally:
            # 发送异常报警信息
            WXMsg(
                msg_content=self._ERROR_MSG.format(job_id=event.job_id, msg=res.msg),
                **self.app.get_object_dict(WXMsg.__name__)
            ).send_wx()


class Cache(BaseCache):

    def delete_cache(self, def_names):
        """
        缓存更新
        :param tuple def_names: 被缓存的函数名
        :return:
        """
        def decorator(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                for def_name in def_names:
                    if def_name:
                        self.delete_memoized(def_name)
                return func(*args, **kwargs)
            return decorated_function
        return decorator


def init_log(project_name, lever, log_dir_name='logs'):
    """
    初始化日志
    :param lever: 日志级别
    :param project_name: 项目名，不可为空
    :param log_dir_name: 日志父目录名
    :return:
    """
    Assert.is_true(is_not_empty(project_name), '初始化日志。项目名不可为空.')
    log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    log_file_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + os.sep + log_dir_name + os.sep + project_name
    FileUtil.creat_dirs(log_file_folder)
    log_file_str = log_file_folder + os.sep + log_file_name

    handler = logging.FileHandler(log_file_str, encoding=Unicode.UTF_8.value)
    handler.setLevel(lever)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    return handler


class CSRFProtect(BaseCSRFProtect):
    """
    CSRF 扩展
    """

    def exempt_views(self, views):
        """
        标记要从CSRF保护中排除的视图或蓝图
        :param views:
        :return:
        """
        Assert.is_true(isinstance(views, tuple) or isinstance(views, list),
                       'the parameters "views" must be lists or tuples.')
        for view in views:
            self.exempt(view)


class Guest(AnonymousUserMixin):
    """
    访客类
    """

    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False


db = SQLAlchemy()
moment = Moment()
migrate = Migrate()
scheduler = APScheduler()
cache = Cache()
login_manager = LoginManager()
csrf = CSRFProtect()
session = Session()

# 自定义未登录跳转路径
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
# login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message_category = 'warning'
# 防止恶意用户篡改 cookies, 当发现 cookies 被篡改时, 该用户的 session 对象会被立即删除, 导致强制重新登录
login_manager.session_protection = 'strong'
login_manager.anonymous_user = Guest

# flask db init
# flask db migrate -m ""
# flask db upgrade
