from dependency_injector.wiring import inject
from flask import session
from flask_socketio import Namespace, join_room

from fiar.data.models import User
from fiar.routes.decorators import socket_context, RouteType, auth_user

GAME_NAMESPACE = '/game'


def game_room_name(game_id: int, user_id: int) -> str:
    return str(game_id) + ':' + str(user_id)


class GameSocket(Namespace):

    @socket_context()
    @auth_user(RouteType.SOCKET)
    @inject
    def on_join_game(self,
                     game_id,
                     auth: User):
        room = game_room_name(game_id, auth.id)
        session['game_id'] = game_id
        join_room(room)

    # @socket_context()
    # @auth_user(RouteType.SOCKET)
    # @inject
    # def on_message(self,
    #                data,
    #                user_service: UserService = Provide[AppContainer.user_service]):
    #     user_service.update_game_active_at(auth)
