from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template

from fiar.di import Container
from fiar.persistence.repositories import UserRepository

bp = Blueprint('main', __name__)


@bp.route('/')
@inject
def lobby(user_repo: UserRepository = Provide[Container.user_repository]):
    users = user_repo.find_all()
    return render_template('lobby.html', users=users)

#
# class Lobby(View):
#     def dispatch_request(self):
#         users = User.query.all()
#         return render_template('users.html', objects=users)
#
# app.add_url_rule('/users/', view_func=ShowUsers.as_view('show_users'))
