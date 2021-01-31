from flask import Flask

import fiar.config
from fiar.cli import register_commands
from fiar.controllers import main, auth
from fiar.controllers.error import register_error_handlers


def create_app() -> Flask:
    app = Flask(__name__)

    # setup config
    app.config.from_object(fiar.config)

    # setup error handlers
    register_error_handlers(app)

    # setup routes
    app.register_blueprint(main.bp, url_prefix='')
    app.register_blueprint(auth.bp, url_prefix='/auth')

    # initialize commands
    register_commands(app)

    return app
