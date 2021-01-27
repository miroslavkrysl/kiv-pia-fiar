from flask import Flask
from flask_injector import FlaskInjector

from fiar.cli import register_commands
from fiar.controllers import auth, main
from fiar.di import modules, initialize_di
from fiar.controllers.error import register_error_handlers


# create and configure the app
from fiar.persistence.db import Database

app = Flask(__name__)

# setup config
app.config.from_pyfile('config.py')

# setup error handlers
register_error_handlers(app)

# setup routes
app.register_blueprint(main.bp, url_prefix='')
app.register_blueprint(auth.bp, url_prefix='/auth')

# initialize commands
register_commands(app)

# initialize dependency injection
di = initialize_di(app)

