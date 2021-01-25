from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from injector import inject

bp = Blueprint('bp', __name__)


@bp.route('/')
def index(db: SQLAlchemy):
    return render_template('index.html')
