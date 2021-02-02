from collections import namedtuple

from flask import Flask

from fiar.cli import register_commands
from fiar.routes import lobby, auth
from fiar.routes.error import register_error_handlers
from fiar.utils import load_config


def create_app() -> Flask:
    app = Flask(__name__)

    # setup config
    config_dict = load_config(app)
    config = namedtuple('Conf', config_dict.keys())(**config_dict)
    app.config.from_object(config)

    # setup error handlers
    register_error_handlers(app)

    # setup routes
    app.register_blueprint(lobby.bp, url_prefix='/')
    app.register_blueprint(auth.bp, url_prefix='/auth')

    # initialize commands
    register_commands(app)

    return app
