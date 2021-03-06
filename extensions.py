#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 扩展实例化
# @Author : Zackeus
# @File : extensions.py 
# @Software: PyCharm
# @Time : 2019/3/21 10:23

import os
import decimal
import logging
import re
import datetime
import codecs
from functools import wraps
from contextlib import contextmanager
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate
from flask_apscheduler import APScheduler as BaseAPScheduler
from apscheduler.events import JobExecutionEvent, EVENT_JOB_ERROR
from flask_caching import Cache as BaseCache
from flask_wtf import CSRFProtect as BaseCSRFProtect
from flask_login import LoginManager as BaseLoginManager, AnonymousUserMixin
from flask_session import Session
from flask.json import JSONEncoder as BaseJsonEncoder

from utils import Assert, is_not_empty, Unicode, MyResponse, WXMsg
from utils.file import FileUtil


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
            with self.app.app_context():
                # 发送异常报警信息
                WXMsg(
                    msg_content=self._ERROR_MSG.format(job_id=event.job_id, msg=res.msg)
                ).send_wx()


class Cache(BaseCache):

    def delete_cache(self, def_names):
        """
        缓存更新
        :param list def_names: 被缓存的函数名
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


class JSONEncoder(BaseJsonEncoder):
    """
    自定义JSON解析器
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return BaseJsonEncoder.default(self, o)


class MyLoggerHandler(logging.FileHandler):

    def __init__(self, filename, when='D', backupCount=0, encoding=None, delay=False, suffix=None, extMatch=None):
        """
        日志
        :param filename: 文件路径
        :param when: 日期 ('M': 一分钟一个文件; 'D': 一天一个文件)
        :param backupCount: 最新保留数; 0为不删除
        :param encoding:
        :param delay:
        :param suffix: 文件名后缀
        :param extMatch: 文件名正则
        """
        self.prefix = filename
        self.when = when.upper()
        # S - Every second a new file
        # M - Every minute a new file
        # H - Every hour a new file
        # D - Every day a new file
        if self.when == 'S':
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
        elif self.when == 'M':
            self.suffix = "%Y-%m-%d_%H-%M"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$"
        elif self.when == 'H':
            self.suffix = "%Y-%m-%d_%H"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}$"
        elif self.when == 'D':
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        if suffix:
            self.suffix = suffix
        if extMatch:
            self.extMatch = extMatch

        self.filefmt = os.path.join("logs", "%s%s" % (self.prefix, self.suffix))
        self.filePath = datetime.datetime.now().strftime(self.filefmt)
        _dir = os.path.dirname(self.filePath)

        # noinspection PyBroadException
        try:
            if os.path.exists(_dir) is False:
                os.makedirs(_dir)
        except Exception:
            print('can not make dirs')
            print('"filepath is " + self.filePath')
            pass

        self.backupCount = backupCount
        if codecs is None:
            encoding = None
        logging.FileHandler.__init__(self, self.filePath, 'a', encoding, delay)

    def shouldChangeFileToWrite(self):
        _filePath = datetime.datetime.now().strftime(self.filefmt)
        if _filePath != self.filePath:
            self.filePath = _filePath
            return 1
        return 0

    def doChangeFile(self):
        self.baseFilename = os.path.abspath(self.filePath)
        if self.stream is not None:
            self.stream.flush()
            self.stream.close()
        if not self.delay:
            self.stream = self._open()
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

    def getFilesToDelete(self):
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = self.prefix + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if re.compile(self.extMatch).match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            if self.shouldChangeFileToWrite():
                self.doChangeFile()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            self.handleError(record)


def init_log(project_name, lever, log_dir_name='logs'):
    """
    初始化日志
    :param lever: 日志级别
    :param project_name: 项目名，不可为空
    :param log_dir_name: 日志父目录名
    :return:
    """
    Assert.is_true(is_not_empty(project_name), '初始化日志。项目名不可为空.')
    log_file_name = 'logger'
    log_file_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + os.sep + log_dir_name + os.sep + project_name
    FileUtil.creat_dirs(log_file_folder)
    log_file = log_file_folder + os.sep + log_file_name

    file_handler = MyLoggerHandler(log_file, when='D', encoding=Unicode.UTF_8.value,
                                   suffix='_%Y-%m-%d.log',
                                   extMatch=r'^_\d{4}-\d{2}-\d{2}.log$')
    file_handler.setLevel(lever)  # 日志输出级别

    fmt = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    formatter = logging.Formatter(fmt)
    file_handler.setFormatter(formatter)
    return file_handler


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


class LoginManager(BaseLoginManager):
    """
    扩展 LoginManager
    """

    def __init__(self, app=None, add_context_processor=True):
        super(self.__class__, self).__init__(app, add_context_processor)
        self._exempt_views = set()
        self._exempt_blueprints = set()
        # 添加静态文件路由过滤
        self._exempt_views.add('flask.helpers.send_static_file')

    def init_app(self, app, add_context_processor=True):
        from utils.decorators import login_required
        super().init_app(app, add_context_processor)

        @app.before_request
        @login_required
        def login_protect():
            """
            登录保护
            :return:
            """
            pass

    def exempt_view(self, view):
        """
        标记要从LoginManager保护中排除的视图或蓝图
        :param view:
        :return:
        """
        if isinstance(view, Blueprint):
            self._exempt_blueprints.add(view.name)
            return view

        if isinstance(view, (str,)):
            view_location = view
        else:
            view_location = '%s.%s' % (view.__module__, view.__name__)
        self._exempt_views.add(view_location)
        return view

    def exempt_views(self, views):
        """
        标记要从LoginManager保护中排除的视图或蓝图
        :param views:
        :return:
        """
        Assert.is_true(isinstance(views, tuple) or isinstance(views, list),
                       'the parameters "views" must be lists or tuples.')
        for view in views:
            self.exempt_view(view)


class Guest(AnonymousUserMixin):
    """
    访客类
    """

    @property
    def id(self):
        return None

    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
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
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'warning'
# login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message_category = 'warning'
# 防止恶意用户篡改 cookies, 当发现 cookies 被篡改时, 该用户的 session 对象会被立即删除, 导致强制重新登录
login_manager.session_protection = 'strong'
login_manager.anonymous_user = Guest


@login_manager.user_loader
def load_user(user_id):
    """
    用户加载函数
    :param user_id:
    :return:
    """
    from models.sys.user import User
    user = User().dao_get(user_id)
    return user


# flask db init
# flask db migrate -m ""
# flask db upgrade
