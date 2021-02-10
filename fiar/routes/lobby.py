from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template, current_app
from flask_socketio import Namespace, join_room

from fiar.db import User
from fiar.di import Container
from fiar.repositories.friendship import FriendshipRepo
from fiar.repositories.friendship_request import FriendshipRequestRepo
from fiar.repositories.user import UserRepo
from fiar.routes.decorators import auth_user, socket_context, socket_auth_user

bp = Blueprint('lobby', __name__)


# --- HTML ---

@bp.route('/')
@auth_user(False)
@inject
def index(auth: User):
    if auth:
        return render_template('lobby.html')

    else:
        return render_template('index.html')


@bp.route('/ajax/players_rows')
@auth_user()
@inject
def players_rows(auth: User,
                 user_repo: UserRepo = Provide[Container.user_repo],
                 friendship_repo: FriendshipRepo = Provide[Container.friendship_repo],
                 friendship_request_repo: FriendshipRequestRepo = Provide[Container.friendship_request_repo]):
    players = user_repo.get_all_online(current_app.config['USER']['ONLINE_TIMEOUT'])

    for player in players:
        player.friendship_included = \
            friendship_request_repo.get_by_users(auth, player) is not None \
            or friendship_request_repo.get_by_users(player, auth)
        player.is_friend = \
            friendship_repo.get_by_users(auth, player) is not None

    return render_template('ajax/players_rows.html', players=players)


@bp.route('/ajax/friends_rows')
@auth_user()
@inject
def friends_rows(auth: User,
                 friendship_repo: FriendshipRepo = Provide[Container.friendship_repo]):
    friendships = friendship_repo.get_all_of(auth)
    return render_template('ajax/friends_rows.html', friendships=friendships)


@bp.route('/ajax/friendship_requests_rows')
@auth_user()
@inject
def friendship_requests_rows(auth: User,
                             friendship_request_repo: FriendshipRequestRepo = Provide[
                                 Container.friendship_request_repo]):
    requests = friendship_request_repo.get_all_of(auth)
    return render_template('ajax/friendship_requests_rows.html', requests=requests)


# --- Socket ---

class LobbySocket(Namespace):
    @socket_context
    @socket_auth_user()
    def on_connect(self,
                   auth: User):
        join_room(auth.id)
