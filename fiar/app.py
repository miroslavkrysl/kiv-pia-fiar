from collections import namedtuple

from flask import Flask
from flask_socketio import SocketIO

from fiar.cli import register_commands
from fiar.routes.api import register_api_routes
from fiar.routes.error import register_error_handlers
from fiar.routes.html import register_html_routes
from fiar.routes.socket import register_socket_routes
from fiar.routes.templating import register_preprocessors
from fiar.utils import load_config


def create_app() -> Flask:
    app = Flask(__name__)

    # setup config
    config_dict = load_config(app)
    config = namedtuple('Conf', config_dict.keys())(**config_dict)
    app.config.from_object(config)

    # setup sockets
    app.socket_io = SocketIO(app)

    # setup template preprocessors
    register_preprocessors(app)

    # setup routes
    register_html_routes(app)
    register_api_routes(app)
    register_socket_routes(app)

    # setup error handlers
    register_error_handlers(app)

    # initialize commands
    register_commands(app)

    return app
