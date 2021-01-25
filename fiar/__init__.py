import os

from flask import Flask, render_template
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy

from fiar import main
from fiar.config import ProductionConfig, DevelopmentConfig
from fiar.di import modules
from fiar.error import register_error_handlers


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # setup config
    app_mode = os.environ.get('APP_MODE', 'production')

    if app_mode == 'production':
        app.config.from_object(ProductionConfig())
    elif app_mode == 'development':
        app.config.from_object(DevelopmentConfig())
    else:
        raise ValueError(f'APP_MODE \'{app_mode}\' not recognized')

    # setup errors
    # register_error_handlers(app)

    # setup routes
    app.register_blueprint(main.bp, url_prefix='')

    # initialize dependency injection
    FlaskInjector(app=app, modules=modules)

    return app
