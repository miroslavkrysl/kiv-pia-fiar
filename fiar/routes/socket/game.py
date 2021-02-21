from dependency_injector.wiring import inject, Provide
from flask import session
from flask_socketio import Namespace, join_room

from fiar.di.container import AppContainer
from fiar.routes.decorators import socket_context, RouteType, auth_user
from fiar.services import auth
from fiar.services.user import UserService

GAME_NAMESPACE = '/game'


class GameSocket(Namespace):

    @socket_context()
    @auth_user(RouteType.SOCKET)
    @inject
    def on_join_game(self,
                     data):
        game_id = data['game_id']
        session['game_id'] = game_id
        join_room(game_id)

    # @socket_context()
    # @auth_user(RouteType.SOCKET)
    # @inject
    # def on_message(self,
    #                data,
    #                user_service: UserService = Provide[AppContainer.user_service]):
    #     user_service.update_game_active_at(auth)
