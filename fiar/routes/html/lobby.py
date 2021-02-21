from datetime import timedelta

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, current_app

from fiar.data.models import User
from fiar.di.container import AppContainer
from fiar.persistence.sqlalchemy.repositories.friendship import FriendshipRepo
from fiar.persistence.sqlalchemy.repositories.invite import InviteRepo
from fiar.persistence.sqlalchemy.repositories.request import RequestRepo
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.routes.decorators import auth_user, RouteType
from fiar.services.friendship import FriendshipService
from fiar.services.game import GameService
from fiar.services.user import UserService

bp = Blueprint('lobby', __name__)


@bp.route('/')
@auth_user(RouteType.HTML, False)
def index(auth: User):
    if auth:
        return render_template('lobby.html')
    else:
        return render_template('index.html')


@bp.route('/ajax/lobby_pane')
@auth_user(RouteType.HTML)
@inject
def lobby_pane(auth: User,
               user_repo: UserRepo = Provide[AppContainer.user_repo],
               user_service: UserService = Provide[AppContainer.user_service],
               friendship_repo: FriendshipRepo = Provide[AppContainer.friendship_repo],
               friendship_service: FriendshipService = Provide[AppContainer.friendship_service],
               game_service: GameService = Provide[AppContainer.game_service],
               invite_repo: InviteRepo = Provide[AppContainer.invite_repo],
               request_repo: RequestRepo = Provide[AppContainer.request_repo]):
    # --- friends users ---
    friendships = friendship_repo.get_all_by_user(auth)
    friends = [friendship.recipient for friendship in friendships]

    for user in friends:
        user.is_online = user_service.is_online(user)
        user.has_sent_invite = game_service.has_received_invite(auth, user)

    # --- online users ---
    online_users = user_repo.get_all_online(timedelta(seconds=current_app.config['USER']['ONLINE_TIMEOUT']))

    # filter out friends and self
    online_users = list(filter(
        lambda u: not friendship_service.are_friends(auth, u) and auth != u, online_users))

    for user in online_users:
        user.is_request_pending = friendship_service.is_request_pending(auth, user)

    # --- invites ---
    invites = invite_repo.get_all_received_by_user(auth)

    # --- requests ---
    requests = request_repo.get_all_by_user(auth)

    return render_template('ajax/lobby_pane.html',
                           requests=requests[:],
                           online_users=online_users[:],
                           invites=invites[:],
                           friends=friends[:])
