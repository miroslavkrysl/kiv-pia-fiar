from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
from injector import Module, singleton, provider
from fiar.db import Db


class DbModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> Db:
        database = Db(app.config['APP_DB_URI'])

        @app.teardown_appcontext
        def shutdown_session(error: Exception):
            database.session.remove()

        return database


class SocketIoModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> SocketIO:
        socket_io = SocketIO(app)
        return socket_io


class LoginManagerModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> LoginManager:
        login_manager = LoginManager(app)
        return login_manager


class MailModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> Mail:
        mail = Mail(app)
        return mail


modules = [
    DbModule,
    SocketIoModule,
    LoginManagerModule,
    MailModule
]
