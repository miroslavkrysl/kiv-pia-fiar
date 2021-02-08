from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template

from fiar.routes.decorators import auth_user, admin_only
from fiar.di import Container
from fiar.repositories.user import UserRepo

bp = Blueprint('game', __name__)


@bp.route('/')
@auth_user
@inject
def index(user_repo: UserRepo = Provide[Container.user_repo]):
    return render_template('lobby.html')
