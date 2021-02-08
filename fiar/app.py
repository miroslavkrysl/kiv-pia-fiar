from collections import namedtuple

from flask import Flask
from flask_socketio import SocketIO

from fiar.cli import register_commands
from fiar.routes import lobby, user, game
from fiar.routes.error import register_error_handlers
from fiar.routes.user import UserSocket
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
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(game.bp, url_prefix='/game')

    # setup sockets
    app.socket_io = SocketIO(app)
    app.socket_io.on_namespace(UserSocket('/user'))

    # initialize commands
    register_commands(app)

    return app
