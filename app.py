import os
from settings import Env, config
from flask import Flask as BasicFlask, current_app
from flask_wtf.csrf import CSRFError

from utils import is_empty, render_info, MyResponse
from views.img import img_bp
from views.test import test_bp
from views.sys.user import user_bp
from views.sys.area import area_bp
from extensions import db, moment, migrate, init_log, scheduler, cache, login_manager, session, csrf
from utils.request import codes
from models import BasicModel, FileModel, AppSys
from models.img import ImgDataModel, ImgDetailModel, ImgTypeModel
from models.audio import AudioLexerModel


class Flask(BasicFlask):

    def get_object_dict(self, o_key):
        """
        根据对象名查询配置参数信息
        :param o_key:
        :return:
        """
        return self.config.get('OBJECT_DICT', {}).get(o_key, {})


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
    # 注册模板过滤器
    register_template_filter(app)
    # 注册模板测试器
    register_template_test(app)

    return app


def register_blueprints(app):
    """
    蓝本初始化
    :param app:
    :return:
    """
    app.register_blueprint(blueprint=img_bp, url_prefix='/img')
    app.register_blueprint(blueprint=user_bp, url_prefix='/user')
    app.register_blueprint(blueprint=area_bp, url_prefix='/sys')
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

    login_manager.init_app(app)
    login_manager.exempt_views((img_bp, test_bp, user_bp))

    session.init_app(app)

    csrf.init_app(app)
    csrf.exempt_views((img_bp, test_bp))

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
    @app.errorhandler(codes.bad)
    def bad_request(e):
        """
        400
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=codes.bad,
                msg='无效的请求'
            ),
            template='errors/400.html',
            status=codes.bad
        )

    @app.errorhandler(codes.not_found)
    def page_not_found(e):
        """
        404
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=codes.not_found,
                msg='资源不存在'
            ),
            template='errors/404.html',
            status=codes.not_found
        )

    @app.errorhandler(codes.not_allowed)
    def not_allowed(e):
        """
        405
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=codes.not_allowed,
                msg='无效的请求头或方法'
            ),
            template='errors/405.html',
            status=codes.not_allowed
        )

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        """
        CSRF验证失败
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=codes.bad,
                msg=e.description if e.description else repr(e)
            ),
            template='errors/400.html',
            status=codes.bad
        )

    @app.errorhandler(codes.unprocessable)
    def handle_validation_error(e):
        """
        422 参数校验错误
        :param e:
        :return:
        """
        return render_info(
            info=MyResponse(
                code=codes.unprocessable,
                msg=e.exc.messages if e.exc else repr(e)
            ),
            template='errors/422.html',
            status=codes.unprocessable
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


def register_template_filter(app):
    """
    自定义过滤器
    :param app:
    :return:
    """

    @app.template_filter('ms_to_time')
    def ms_to_time(ms):
        """
        毫秒转时间格式
        :param ms:
        :return:
        """
        from utils import ms_to_time as ms_to_time_util
        return ms_to_time_util(ms)

    @app.template_filter('lexer_label')
    def lexer_label(text, items):
        """
        语义标签过滤
        :param str text:
        :param list items:
        :return:
        """
        _ne_list = [
            {'code': 'PER', 'title': '人名', 'color': '#FFCC33'},
            {'code': 'LOC', 'title': '地名', 'color': '#FF9933'},
            {'code': 'ORG', 'title': '机构名', 'color': '#FF6633'},
            {'code': 'TIME', 'title': '时间', 'color': '#FFFF00'},
            {'code': 'TBW', 'title': '忌讳语', 'color': '#FF0000'},
            {'code': 'TOA', 'title': '汽车品牌', 'color': '#CC0000'},
        ]
        _item = '<font class="{ne} lexer_font_show" color="#FF0000">{item}</font>'
        if is_empty(items):
            return text
        for item in items:
            text = text.replace(item.item, _item.format(ne=item.ne, item=item.item))
        return text


def register_template_test(app):
    """
    自定义测试器
    :param app:
    :return:
    """

    @app.template_test(name='odd')
    def odd(n):
        """
        判断是否为基数
        :param int n:
        :return:
        """
        from utils import is_odd
        return is_odd(n)


