from flask import Flask

from fiar.routes.socket.game import GAME_NAMESPACE, GameSocket
from fiar.routes.socket.lobby import LobbySocket, LOBBY_NAMESPACE
from fiar.routes.socket.user import UserSocket, USER_NAMESPACE


def register_socket_routes(app: Flask):
    app.socket_io.on_namespace(UserSocket(USER_NAMESPACE))
    app.socket_io.on_namespace(LobbySocket(LOBBY_NAMESPACE))
    app.socket_io.on_namespace(GameSocket(GAME_NAMESPACE))
