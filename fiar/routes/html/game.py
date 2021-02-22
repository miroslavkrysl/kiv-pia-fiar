from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, abort, current_app

from fiar.data.models import User
from fiar.di.container import AppContainer
from fiar.persistence.sqlalchemy.repositories.game import GameRepo
from fiar.persistence.sqlalchemy.repositories.move import MoveRepo
from fiar.routes.decorators import auth_user, RouteType
from fiar.services.game import GameService

bp = Blueprint('game', __name__)


@bp.route('/<int:id>')
@auth_user(RouteType.HTML)
@inject
def index(id: int,
          auth: User,
          game_service: GameService = Provide[AppContainer.game_service],
          game_repo: GameRepo = Provide[AppContainer.game_repo]):
    game = game_repo.get_by_id(id)

    if game is None:
        return abort(404, description=f'Game with id {id} does not exist')

    side = game_service.get_player_side(game, auth)
    if side is None:
        return abort(403, 'You are not in this game')

    return render_template('game/game.html', game=game, side=side)


@bp.route('/ajax/game_pane/<int:id>')
@auth_user(RouteType.HTML)
@inject
def get_game_pane(id: int,
                  auth: User,
                  game_service: GameService = Provide[AppContainer.game_service],
                  move_repo: MoveRepo = Provide[AppContainer.move_repo],
                  game_repo: GameRepo = Provide[AppContainer.game_repo]):
    game = game_repo.get_by_id(id)

    if game is None:
        return abort(404, description=f'Game with id {id} does not exist')

    side = game_service.get_player_side(game, auth)
    if side is None:
        return abort(403, 'You are not in this game')

    moves = move_repo.get_all_by_game(game)

    board_size = current_app.config['GAME']['BOARD_SIZE']
    board = [[{'col': col, 'row': row, 'side': None} for col in range(0, board_size)] for row in range(0, board_size)]

    for move in moves:
        board[move.row][move.col]['side'] = move.side

    return render_template('ajax/game_pane.html', game=game, side=side, board=board)
