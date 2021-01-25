from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, provider, singleton


class DbModule(Module):
    @provider
    @singleton
    def provide(self, app: Flask) -> SQLAlchemy:
        db = SQLAlchemy(app)
        return db


modules = [DbModule]
