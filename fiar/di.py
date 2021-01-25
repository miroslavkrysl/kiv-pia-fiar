from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton, provider


class DbModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> SQLAlchemy:
        db = SQLAlchemy(app)
        return db


modules = [DbModule]
