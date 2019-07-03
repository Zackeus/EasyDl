import os
from settings import Env, config
from flask import Flask as BasicFlask, current_app
from flask_wtf.csrf import CSRFError

from utils import is_empty, render_info, MyResponse
from views import demo_bp
from views.ai import img_bp, audio_bp
from views.sys import user_bp, area_bp, menu_bp, dict_bp, file_bp
from views.api import img_api_bp
from extensions import db, moment, migrate, init_log, scheduler, cache, login_manager, session, csrf
from utils.request import codes
from models.audio import AudioLexerNeModel


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
    app.register_blueprint(blueprint=area_bp, url_prefix='/sys')
    app.register_blueprint(blueprint=user_bp, url_prefix='/sys/user')
    app.register_blueprint(blueprint=menu_bp, url_prefix='/sys/menu')
    app.register_blueprint(blueprint=dict_bp, url_prefix='/sys/dict')
    app.register_blueprint(blueprint=file_bp, url_prefix='/sys/file')

    app.register_blueprint(blueprint=img_bp, url_prefix='/ai/img')
    app.register_blueprint(blueprint=audio_bp, url_prefix='/audio')
    app.register_blueprint(blueprint=demo_bp, url_prefix='/demo')

    app.register_blueprint(blueprint=img_api_bp, url_prefix='/api/img')


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
    # 登录过滤保护
    login_manager.exempt_views((user_bp, demo_bp, audio_bp, img_api_bp))

    session.init_app(app)

    csrf.init_app(app)
    # csrf过滤保护
    csrf.exempt_views((demo_bp, audio_bp, img_api_bp))

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

    @app.template_filter('filter_none')
    def filter_none(v):
        """
        空值过滤
        :param v:
        :return:
        """
        return '' if v is None else v

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
        _item = '<font id="{id}" class="{ne} lexer_font_show" color="{color}" data-ne-title="{ne_title}">{item}</font>'
        _ne_key = 'ne_{0}'

        if is_empty(items):
            return text

        ne_dict = {}
        for item in items:
            lexer = AudioLexerNeModel().dao_get_by_code(item.ne)  # type: AudioLexerNeModel

            ne_key = '{' + _ne_key.format(str(item.byte_offset)) + '}'
            text = text.replace(item.item, ne_key, 1)
            ne_dict.update(
                {_ne_key.format(str(item.byte_offset)): _item.format(
                    id=item.id,
                    ne=item.ne,
                    color=lexer.color,
                    ne_title=lexer.title,
                    item=item.item
                )}
            )
        return text.format_map(ne_dict)


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

    @app.template_test(name='empty')
    def empty(o):
        """
        判断是否为空
        :param o:
        :return:
        """
        return True if is_empty(o) else False


