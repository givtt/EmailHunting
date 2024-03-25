from flask import Flask
from .apps.EmailService import EmailService
import logging


EmailServer = EmailService()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.app_context().push()

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    EmailServer.load_config()

    from .routes.auth import auth
    from .routes.main import main
    from .routes.setting import setting

    app.register_blueprint(auth, url_prefix="/auth/")
    app.register_blueprint(setting, url_prefix="/setting/")
    app.register_blueprint(main, url_prefix="/")

    return app

