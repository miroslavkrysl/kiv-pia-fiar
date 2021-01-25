from flask import Flask
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


modules = [DbModule, SocketIoModule]
