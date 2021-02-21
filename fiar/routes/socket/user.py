from dependency_injector.wiring import inject, Provide
from flask_socketio import Namespace, emit

from fiar.data.models import User
from fiar.di.container import AppContainer
from fiar.routes.decorators import socket_context, auth_user, RouteType
from fiar.routes.socket import LOBBY_NAMESPACE
from fiar.routes.socket.lobby import LOBBY_ROOM
from fiar.services.user import UserService

USER_NAMESPACE = '/user'


class UserSocket(Namespace):
    @socket_context()
    @auth_user(RouteType.SOCKET)
    @inject
    def on_connect(self):
        emit('new_online_user', to=LOBBY_ROOM, include_self=False, namespace=LOBBY_NAMESPACE)

    @socket_context()
    @auth_user(RouteType.SOCKET)
    @inject
    def on_active(self,
                  data,
                  auth: User,
                  user_service: UserService = Provide[AppContainer.user_service]):
        user_service.update_last_active_at(auth)
