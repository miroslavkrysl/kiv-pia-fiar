import os

from flask import Flask, render_template
from flask_injector import FlaskInjector

from fiar import main, auth, config
from fiar.db import init_db_command
from fiar.di import modules
from fiar.error import register_error_handlers


# create and configure the app
app = Flask(__name__)

# setup config
app.config.from_pyfile('config.py')

# setup error handlers
register_error_handlers(app)

# setup routes
app.register_blueprint(main.bp, url_prefix='')
app.register_blueprint(auth.bp, url_prefix='/auth')

# initialize commands
app.cli.add_command(init_db_command)

# initialize dependency injection
di = FlaskInjector(app=app, modules=modules)
