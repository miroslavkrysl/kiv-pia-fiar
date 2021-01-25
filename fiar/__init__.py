import os

from flask import Flask
from flask_injector import FlaskInjector

from fiar import main
from fiar.config import ProductionConfig, DevelopmentConfig
from fiar.di import modules


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app_mode = os.environ.get('APP_MODE', 'production')

    if app_mode == 'production':
        app.config.from_object(ProductionConfig())
    elif app_mode == 'development':
        app.config.from_object(DevelopmentConfig())
    else:
        raise ValueError(f'APP_MODE \'{app_mode}\' not recognized')

    app.register_blueprint(main.bp, url_prefix='')
    FlaskInjector(app=app, modules=modules)

    return app
