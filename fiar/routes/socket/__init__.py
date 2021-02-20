from flask import Flask

from fiar.routes.socket.lobby import LobbySocket
from fiar.routes.socket.user import UserSocket

LOBBY_NAMESPACE = '/lobby'
GAME_NAMESPACE = '/game'
USER_NAMESPACE = '/user'


def register_socket_routes(app: Flask):
    app.socket_io.on_namespace(UserSocket(USER_NAMESPACE))
    app.socket_io.on_namespace(LobbySocket(LOBBY_NAMESPACE))
