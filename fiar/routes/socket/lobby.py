from flask_socketio import Namespace, join_room

from fiar.data.models import User
from fiar.routes.decorators import socket_context, auth_user, RouteType


class LobbySocket(Namespace):
    @socket_context()
    @auth_user(RouteType.SOCKET)
    def on_connect(self,
                   auth: User):
        join_room(auth.id)
