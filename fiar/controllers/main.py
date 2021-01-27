from flask import Blueprint, render_template

from fiar.persistence.models import User
from fiar.persistence.repositories import UserRepository

bp = Blueprint('main', __name__)

i = 0


@bp.route('/')
def index(user_repo: UserRepository):
    global i
    users = user_repo.all()
    user_repo.add(User(username="hello" + str(i)))
    i += 1
    return render_template('index.html', users=users)
