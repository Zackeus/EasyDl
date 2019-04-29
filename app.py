import os
import requests
from settings import Env, config
from flask import Flask as BasicFlask, current_app
from flask_wtf.csrf import CSRFError

from views.loan import loan_bp
from views.test import test_bp
from views.sys.user import user_bp
from extensions import db, moment, migrate, init_log, scheduler, cache
from utils.response import MyResponse, render_info
from utils.object_util import is_empty
from utils.str_util import EncodingFormat
from models.basic import BasicModel
from models.loan.loan_file import LoanFileModel
from models.loan.loan_type import LoanTypeModel
from models.loan.flow_type import FlowTypeModel
from models.loan.img_type import ImgTypeModel
from models.loan.img_detail import ImgDetailModel
from models.file import FileModel


class Flask(BasicFlask):

    def get_object_dict(self, o_name):
        """
        根据对象名查询配置参数信息
        :param o_name:
        :return:
        """
        o_name = EncodingFormat.hump_to_pep8(o_name).upper()
        return self.config.get(o_name, {})


def create_app(config_name=None):
    """
    工厂函数
    :param config_name:
    :return:
    """
    if is_empty(config_name) or config_name not in [env.value for env in Env]:
        config_name = os.getenv('FLASK_CONFIG', Env.DEVELOPMENT.value)

    app = Flask(import_name=__name__)

    # 加载配置
    app.config.from_object(obj=config[config_name])
    # 注册日志
    app.logger.addHandler(init_log(app.config.get('PROJECT_NAME', None), app.config.get('LOGGER_LEVER', None)))

    # 注册扩展
    register_extensions(app)
    # 注册蓝本
    register_blueprints(app)
    # 注册错误处理函数
    register_errors(app)
    # 注册shell上下文处理函数
    register_shell_context(app)
    # 注册模板上下文处理函数
    register_template_context(app)

    return app


def register_blueprints(app):
    """
    蓝本初始化
    :param app:
    :return:
    """
    app.register_blueprint(blueprint=loan_bp, url_prefix='/loan')
    app.register_blueprint(blueprint=user_bp, url_prefix='/user')
    app.register_blueprint(blueprint=test_bp, url_prefix='/test')


def register_extensions(app):
    """
    扩展实例化
    :param app:
    :return:
    """
    db.init_app(app)
    moment.init_app(app)
    migrate.init_app(app=app, db=db)
    cache.init_app(app)

    # 定时任务 解决FLASK DEBUG模式定时任务执行两次
    if os.environ.get('FLASK_DEBUG', '0') == '0':
        scheduler.init_app(app)
        scheduler.start()
    elif os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.init_app(app)
        scheduler.start()


def register_errors(app):
    """
    错误函数初始化
    :param app:
    :return:
    """
    @app.errorhandler(requests.codes.bad)
    def bad_request(e):
        """
        400
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=requests.codes.bad,
                msg='无效的请求'
            ),
            template='errors/400.html',
            status=requests.codes.bad
        )

    @app.errorhandler(requests.codes.not_found)
    def page_not_found(e):
        """
        404
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=requests.codes.not_found,
                msg='资源不存在'
            ),
            template='errors/404.html',
            status=requests.codes.not_found
        )

    @app.errorhandler(requests.codes.not_allowed)
    def not_allowed(e):
        """
        405
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=requests.codes.not_allowed,
                msg='无效的请求头或方法'
            ),
            template='errors/405.html',
            status=requests.codes.not_allowed
        )

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_info(
            info=MyResponse.init_error(e),
            template='errors/400.html',
            status=requests.codes.bad
        )

    @app.errorhandler(requests.codes.unprocessable)
    def handle_validation_error(e):
        """
        422 参数校验错误
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=requests.codes.unprocessable,
                msg=e.exc.messages if e.exc else repr(e)
            ),
            template='errors/422.html',
            status=requests.codes.unprocessable
        )

    @app.errorhandler(Exception)
    def handle_unknown_error(e):
        """
        未知的异常
        :param e:
        :return:
        """
        try:
            return render_info(info=MyResponse.init_error(e), template='errors/500.html')
        finally:
            # 记录日志
            current_app.logger.exception(e)


def register_shell_context(app):
    """
    shell上下文初始化
    :param app:
    :return:
    """
    pass


def register_template_context(app):
    """
    模板上下文初始化
    :param app:
    :return:
    """
    pass
