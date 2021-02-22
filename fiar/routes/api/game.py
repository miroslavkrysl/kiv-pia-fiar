import json

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from flask_socketio import emit
from marshmallow import ValidationError

from fiar.data.models import User, MoveResult
from fiar.data.schemas import game_schema, move_schema, invite_schema
from fiar.di.container import AppContainer
from fiar.persistence.sqlalchemy.repositories.game import GameRepo
from fiar.persistence.sqlalchemy.repositories.invite import InviteRepo
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.routes.decorators import auth_user, RouteType
from fiar.routes.socket import LOBBY_NAMESPACE
from fiar.routes.socket.game import GAME_NAMESPACE, game_room_name
from fiar.services.game import GameService

bp = Blueprint('game_api', __name__)


# --- Game ---

@bp.route('/game/<int:opponent_id>', methods=['POST'])
@auth_user(RouteType.API)
@inject
def post_game(opponent_id: int,
              auth: User,
              user_repo: UserRepo = Provide[AppContainer.user_repo],
              game_service: GameService = Provide[AppContainer.game_service]):
    opponent = user_repo.get_by_id(opponent_id)

    if opponent is None:
        return jsonify({'error': f'User with id {opponent_id} does not exist'}), 404

    if not game_service.has_received_invite(auth, opponent):
        return jsonify({'error': 'Invite not received from the other user.'}), 409

    game = game_service.accept_invite(auth, opponent)

    emit('invite_accepted', game.id, to=opponent_id, namespace=LOBBY_NAMESPACE)

    return jsonify(game_schema.dump(game)), 201


@bp.route('/surrender/<int:game_id>', methods=['POST'])
@auth_user(RouteType.API)
@inject
def post_surrender(game_id: int,
                   auth: User,
                   game_repo: GameRepo = Provide[AppContainer.game_repo],
                   game_service: GameService = Provide[AppContainer.game_service]):
    game = game_repo.get_by_id(game_id)

    if game is None:
        return jsonify({'error': f'Game with id {game_id} does not exist'}), 404

    side = game_service.get_player_side(game, auth)
    if side is None:
        return jsonify({'error': 'You are not in this game.'}), 403

    if game_service.is_ended(game):
        return jsonify({'error': 'Already ended.'}), 412

    game_service.surrender(game, side)

    room = game_room_name(game_id, game_service.opponent_id(game, side))
    emit('opponent_surrendered', to=room, namespace=GAME_NAMESPACE)

    return jsonify(), 200


# --- Move ---

@bp.route('/move/<int:game_id>', methods=['POST'])
@auth_user(RouteType.API)
@inject
def post_move(game_id: int,
              auth: User,
              game_repo: GameRepo = Provide[AppContainer.game_repo],
              game_service: GameService = Provide[AppContainer.game_service]):
    game = game_repo.get_by_id(game_id)

    if game is None:
        return jsonify({'error': f'Game with id {game_id} does not exist'}), 404

    try:
        data = move_schema.load(request.form)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    side = game_service.get_player_side(game, auth)
    if side is None:
        return jsonify({'error': 'You are not in this game.'}), 403

    if game_service.is_ended(game):
        return jsonify({'error': 'Game is ended.'}), 412

    if not game_service.is_on_turn(game, side):
        return jsonify({'error': 'You are not on turn.'}), 412

    result = game_service.do_move(game, side, data['row'], data['col'])
    if result == MoveResult.OUT:
        code = 400
    elif result == MoveResult.OCCUPIED:
        code = 409
    else:
        room = game_room_name(game_id, game_service.opponent_id(game, side))
        emit('opponent_played', result.value, to=room, namespace=GAME_NAMESPACE)
        code = 201

    return jsonify({'result': result.value}), code


# --- Invite ---

@bp.route('/invite/<int:opponent_id>', methods=['POST'])
@auth_user(RouteType.API)
@inject
def post_invite(opponent_id: int,
                auth: User,
                user_repo: UserRepo = Provide[AppContainer.user_repo],
                game_service: GameService = Provide[AppContainer.game_service]):
    opponent = user_repo.get_by_id(opponent_id)

    if opponent is None:
        return jsonify({'error': f'User with id {opponent_id} does not exist'}), 400

    if game_service.has_received_invite(auth, opponent):
        return jsonify({'error': 'Already requested from the other user'}), 409

    if game_service.has_received_invite(opponent, auth):
        return jsonify(), 200

    game_service.create_invite(auth, opponent)

    emit('invite_received', to=opponent_id, namespace=LOBBY_NAMESPACE)

    return jsonify(), 201


@bp.route('/invite/<int:opponent_id>', methods=['DELETE'])
@auth_user(RouteType.API)
@inject
def delete_invite(opponent_id: int,
                  auth: User,
                  user_repo: UserRepo = Provide[AppContainer.user_repo],
                  invite_repo: InviteRepo = Provide[AppContainer.invite_repo],
                  game_service: GameService = Provide[AppContainer.game_service]):
    opponent = user_repo.get_by_id(opponent_id)

    if opponent is None:
        return jsonify({'error': f'User with {opponent_id} does not exist'}), 404

    if game_service.has_received_invite(auth, opponent):
        invite = invite_repo.get_by_users(opponent, auth)
        invite_repo.delete(invite)
        emit('invite_refused', to=opponent_id, namespace=LOBBY_NAMESPACE)
    elif game_service.has_received_invite(opponent, auth):
        invite = invite_repo.get_by_users(auth, opponent)
        invite_repo.delete(invite)
        emit('invite_deleted', to=opponent_id, namespace=LOBBY_NAMESPACE)

    return jsonify(), 200
