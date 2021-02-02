from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template

from fiar.di import Container
from fiar.repositories.user import UserRepo

bp = Blueprint('lobby', __name__)


@bp.route('')
@inject
def index(user_repo: UserRepo = Provide[Container.user_repo]):
    users = user_repo.get_all()
    return render_template('lobby.html', users=users)
