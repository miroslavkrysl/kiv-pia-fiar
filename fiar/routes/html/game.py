from flask import Blueprint

bp = Blueprint('game', __name__)


# from dependency_injector.wiring import Provide, inject
# from flask import Blueprint, render_template
#
# from fiar.di.di import Container
# from fiar.data.repositories.user import UserRepo
#
# bp = Blueprint('game', __name__)
#
#
# @bp.route('/')
# @inject
# def index(user_repo: UserRepo = Provide[Container.user_repo]):
#     return render_template('game/game.html')
#
#
# @bp.route('/ajax/game_board')
# @inject
# def game_board():
#     moves = [
#         {'x': 4, 'y': 4, 'player': 0},
#         {'x': 1, 'y': 1, 'player': 1},
#         {'x': 7, 'y': -6, 'player': 0},
#         {'x': 2, 'y': -1, 'player': 1},
#         {'x': -4, 'y': 4, 'player': 0},
#         {'x': -1, 'y': -4, 'player': 1}
#     ]
#     base = {
#         'y': -7,
#         'x': -7
#     }
#     board = [[{'x': x, 'y': y, 'player': None} for x in range(0, 15)] for y in range(0, 15)]
#
#     for move in moves:
#         cell = board[move['y'] - base['y']][move['x'] - base['x']]
#         cell['player'] = move['player']
#
#     return render_template('ajax/game_board.html', board=board)
#
