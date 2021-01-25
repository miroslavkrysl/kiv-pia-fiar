from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from injector import inject

bp = Blueprint('bp', __name__)


@bp.route('/')
def index(db: SQLAlchemy):
    return 'Hello world index'
