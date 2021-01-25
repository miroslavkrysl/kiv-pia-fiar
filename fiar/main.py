from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('main', __name__)


@bp.route('/')
def index(db: SQLAlchemy):
    return render_template('index.html')
