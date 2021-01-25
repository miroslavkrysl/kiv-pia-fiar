from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton, provider


class DbModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> SQLAlchemy:
        db = SQLAlchemy(app)
        return db


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
