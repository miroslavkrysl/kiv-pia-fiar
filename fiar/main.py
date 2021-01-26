from flask import Blueprint, render_template

from fiar.db import Db

bp = Blueprint('main', __name__)


@bp.route('/')
def index(db: Db):
    return render_template('index.html')
