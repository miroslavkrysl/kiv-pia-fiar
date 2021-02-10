from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template
from flask_socketio import Namespace

from fiar.di import Container
from fiar.repositories.user import UserRepo
from fiar.routes.decorators import socket_context, socket_auth_user

bp = Blueprint('game', __name__)


@bp.route('/')
@inject
def index(user_repo: UserRepo = Provide[Container.user_repo]):
    return render_template('game/game.html')


@bp.route('/ajax/game_board')
@inject
def game_board():
    moves = [
        {'x': 4, 'y': 4, 'player': 0},
        {'x': 1, 'y': 1, 'player': 1},
        {'x': 7, 'y': -6, 'player': 0},
        {'x': 2, 'y': -1, 'player': 1},
        {'x': -4, 'y': 4, 'player': 0},
        {'x': -1, 'y': -4, 'player': 1}
    ]
    base = {
        'y': -7,
        'x': -7
    }
    board = [[{'x': x, 'y': y, 'player': None} for x in range(0, 15)] for y in range(0, 15)]

    for move in moves:
        cell = board[move['y'] - base['y']][move['x'] - base['x']]
        cell['player'] = move['player']

    return render_template('ajax/game_board.html', board=board)


# --- Socket ---

# class GameSocket(Namespace):
#
#     @socket_context
#     @socket_auth_user()
#     @inject
#     def on_join_game(self,
#                   data,
#                   game_service: GameService = Provide[Container.user_service]):
#
#         game_id = data['message']
#
#
#     @socket_context
#     @socket_auth_user()
#     @inject
#     def on_message(self,
#                   data,
#                   user_service: UserService = Provide[Container.user_service]):
#         user_service.update_last_active_at(auth)