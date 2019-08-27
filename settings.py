#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : settings.py 
# @Software: PyCharm
# @Time : 2019/3/21 10:02


import redis
import logging
import datetime
import os
from enum import Enum, unique
from utils.file.file import FileUtil
from utils.object_util import is_empty
from utils.config_util import ConfigUtils


base_dir = os.path.abspath(path=os.path.dirname(__file__))
base_static = os.path.join(base_dir, 'static')


def init_object_dict():
    """
    从配置文件初始化字典
    :return:
    """
    object_dict = {}
    file_paths = FileUtil.get_files_by_suffix(base_static, ['cfg', ])
    if is_empty(file_paths):
        return object_dict
    for file_path in file_paths:
        object_dict.update(ConfigUtils(file_path).get_config_dict())
    return object_dict


@unique
class Env(Enum):
    """
    项目环境
    """
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'


class BaseConfig(object):
    """ 基本配置类 """

    # 项目名
    PROJECT_NAME = 'EasyDl'

    # 客户端的cookie的名称
    SESSION_COOKIE_NAME = 'session_token'
    # 保存到session中的值的前缀
    SESSION_KEY_PREFIX = '{0}-session:'.format(os.getenv('PROJECT_NAME', PROJECT_NAME))
    SECRET_KEY = os.getenv('SECRET_KEY', 'EA2yCN6eBn4mDfA5')
    # 为cookie设置签名来保护数据不被更改
    SESSION_USE_SIGNER = True
    # 设置 session 有效时长
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=3)
    SESSION_TYPE = 'redis'

    # 关闭 JSON ascii编码，使其支持中文
    JSON_AS_ASCII = False

    # 关闭 Debug 拦截重定向请求
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # 关闭警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 启用查询记录
    SQLALCHEMY_RECORD_QUERIES = True
    # 数据库连接池大小
    SQLALCHEMY_POOL_SIZE = 15
    # 数据库连接池的超时时间
    SQLALCHEMY_POOL_TIMEOUT = 30
    # 自动循环连接的秒数, 定时重连接
    SQLALCHEMY_POOL_RECYCLE = 1800
    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃
    SQLALCHEMY_MAX_OVERFLOW = 20

    # 缓存类型
    CACHE_TYPE = 'redis'
    # 缓存的前缀
    CACHE_KEY_PREFIX = '{0}-cache:'.format(os.getenv('PROJECT_NAME', PROJECT_NAME))
    # redis 服务器端口
    CACHE_REDIS_PORT = 6379
    # redis 的 db 库
    CACHE_REDIS_DB = 0
    # 默认缓存时间 单位秒
    CACHE_DEFAULT_TIMEOUT = 60 * 60 * 24 * 3

    # 开启CSRFProtect
    CKEDITOR_ENABLE_CSRF = True
    # CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    # 定时任务
    SCHEDULER_API_ENABLED = True

    # 用于发送邮件的 SMTP 服务器
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.163.com')
    # 发送端口
    MAIL_PORT = 465
    # 是否使用 STARTTLS
    # MAIL_USE_TLS=False
    # 是否使用 SSL/TLS
    MAIL_USE_SSL = True
    # 发信服务器的用户名
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'loan_yulon_finance@163.com')
    # 发信服务器的密码
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'syr391592723')
    # 默认的发信人
    MAIL_DEFAULT_SENDER = ('YuLon', os.getenv('MAIL_USERNAME', 'loan_yulon_finance@163.com'))

    # 序列化对象字典
    OBJECT_DICT = init_object_dict()

    # 贷款路径秘钥
    DATA_PATH_KEY = os.getenv('LOAN_PATH_KEY', 'xatmTsm7GAmFcRet')
    # 资料存放目录
    DATA_DIR = 'D:/FileData'
    # 图片资料文件夹
    DATA_DIR_IMG = 'Img'
    # OCR 资料存放目录
    OCR_FILE_DIR = 'D:/OcrFile'

    # JOBS = [
    #     {
    #         'id': 'img_ocr',
    #         'func': 'jobs.img:img_ocr',
    #         'args': (8, ),
    #         'trigger': 'cron',
    #         # 'second': '0/10',
    #         'minute': '0/3',
    #         # 'hour': '8-20',
    #         'max_instances': 1,
    #         'coalesce': True,
    #         'misfire_grace_time': 1800
    #     },
    #     {
    #         'id': 'img_push',
    #         'func': 'jobs.img:img_push',
    #         'trigger': 'cron',
    #         # 'second': '0/10',
    #         'minute': '0/3',
    #         # 'hour': '8-20',
    #         'max_instances': 1,
    #         'coalesce': True,
    #         'misfire_grace_time': 1800
    #     }
    # ]


class DevelopmentConfig(BaseConfig):
    """ 开发配置类 """

    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379', password='syr391592723*')

    # 日志级别
    LOGGER_LEVER = logging.DEBUG

    # 输出sql语句
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mssql+pymssql://sa:m4bj/6fu4u,4@10.5.60.90:1433/EASY_DL')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mssql+pymssql://sa:syr391592723*@127.0.0.1:1433/EASY_DL')
    SQLALCHEMY_BINDS = {
        'YFC_UCL_PRD': 'oracle://YFC_UCL_PRD:yulon2016@10.5.60.132:1521/credit',
        'JEESITE-YFC': 'mssql+pymssql://sa:syr391592723*@127.0.0.1:1433/jeesite-yfc'
    }

    # redis 度武器主机
    CACHE_REDIS_HOST = '127.0.0.1'
    # redis 服务器密码
    CACHE_REDIS_PASSWORD = 'syr391592723*'

    # 关闭CSRF保护
    # WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    """ 测试配置类 """

    # 日志级别
    LOGGER_LEVER = logging.DEBUG

    TESTING = True
    # WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mssql+pymssql://sa:m4bj/6fu4u,4@10.5.60.90:1433/EASY_DL_BACKUP')
    SQLALCHEMY_BINDS = {
        'YFC_UCL_PRD': 'oracle://YFC_UCL_PRD:yulon2016@10.5.60.132:1521/credit',
        'JEESITE-YFC': 'mssql+pymssql://sa:m4bj/6fu4u,4@10.5.60.80:1433/jeesite-yfc'
    }


class ProductionConfig(BaseConfig):
    """ 生产配置类 """

    SESSION_REDIS = redis.Redis(host='10.5.60.77', port='6379', password='syr391592723*')

    # 日志级别
    LOGGER_LEVER = logging.WARNING
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mssql+pymssql://sa:m4bj/6fu4u,4@10.5.60.90:1433/EASY_DL')
    SQLALCHEMY_BINDS = {
        'YFC_UCL_PRD': 'oracle://YFC_UCL_PRD:yulon2016@10.5.60.132:1521/credit',
        'JEESITE-YFC': 'mssql+pymssql://sa:m4bj/6fu4u,4@10.5.60.80:1433/jeesite-yfc'
    }

    # redis 度武器主机
    CACHE_REDIS_HOST = '10.5.60.77'
    # redis 服务器密码
    CACHE_REDIS_PASSWORD = 'syr391592723*'


config = {
    Env.DEVELOPMENT.value: DevelopmentConfig,
    Env.TESTING.value: TestingConfig,
    Env.PRODUCTION.value: ProductionConfig
}

