from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from fiar.data.models import User, MoveResult
from fiar.data.schemas import game_schema, move_schema
from fiar.di.container import AppContainer
from fiar.persistence.sqlalchemy.repositories.game import GameRepo
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.routes.decorators import auth_user, RouteType
from fiar.services.game import GameService

bp = Blueprint('game_api', __name__)


# # --- Friends ---
#
# class UserWithOnlineSchema(UserSchema):
#     is_online = fields.Boolean()
#
#
# user_with_online_schema = UserWithOnlineSchema()
#
#
# @bp.route('/friends', methods=['GET'])
# @auth_user(RouteType.API)
# @inject
# def get_friends(auth: User,
#                 user_service: UserService = Provide[AppContainer.user_service],
#                 friendship_repo: FriendshipRepo = Provide[AppContainer.friendship_repo]):
#     friends = friendship_repo.get_all_friends_sent_by(auth)
#
#     for friend in friends:
#         friend.is_online = user_service.is_online(friend)
#
#     return jsonify(user_schema.dump(friends, many=True))
#
#
# # --- Friends requested ---
#
# @bp.route('/friends_requested', methods=['GET'])
# @auth_user(RouteType.API)
# @inject
# def get_friends_requested(auth: User,
#                           friendship_request_repo: FriendshipRequestRepo = Provide[
#                               AppContainer.request_repo]):
#     users = friendship_request_repo.get_all_users_requested_by(auth)
#
#     return jsonify(user_schema.dump(users, many=True))
#
#
# # --- Friends received ---
#
# @bp.route('/friends_received', methods=['GET'])
# @auth_user(RouteType.API)
# @inject
# def get_friends_received(auth: User,
#                          friendship_request_repo: FriendshipRequestRepo = Provide[
#                              AppContainer.request_repo]):
#     users = friendship_request_repo.get_all_users_received_by(auth)
#
#     return jsonify(user_schema.dump(users, many=True))


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
        return jsonify({'error': f'User with id {opponent_id} does not exist'}), 400

    if not game_service.has_received_invite(auth, opponent):
        return jsonify({'error': 'Invite not received from the other user.'}), 409

    game = game_service.accept_invite(auth, opponent)

    return jsonify(game_schema.dump(game)), 201


# --- Move ---

@bp.route('/move/<int:game_id>', methods=['PUT'])
@auth_user(RouteType.API)
@inject
def put_move(game_id: int,
             auth: User,
             game_repo: GameRepo = Provide[AppContainer.game_repo],
             game_service: GameService = Provide[AppContainer.game_service]):
    game = game_repo.get_by_id(game_id)

    if game is None:
        return jsonify({'error': f'User with {game_id} does not exist'}), 404

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
        code = 201

    return jsonify({'result': result.value}), code

#
#
# @bp.route('/friendship/<int:id>', methods=['DELETE'])
# @auth_user(RouteType.API)
# @inject
# def delete_friendship(id: int,
#                       auth: User,
#                       user_repo: UserRepo = Provide[AppContainer.user_repo],
#                       friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
#     friend = user_repo.get_by_id(id)
#
#     if friend is None:
#         return jsonify({'error': f'User with {id} does not exist'}), 404
#
#     if friendship_service.are_friends(auth, friend):
#         friendship_service.remove_friendship(auth, friend)
#
#     return jsonify(), 200
#
#
# # --- Invite ---
#
# @bp.route('/invite/<int:id>', methods=['PUT'])
# @auth_user(RouteType.API)
# @inject
# def put_request(id: int,
#                 auth: User,
#                 user_repo: UserRepo = Provide[AppContainer.user_repo],
#                 game_service: GameService = Provide[AppContainer.game_service]):
#     friend = user_repo.get_by_id(id)
#
#     if friend is None:
#         return jsonify({'error': f'User with id {id} does not exist'}), 400
#
#     if friendship_service.has_received_request(auth, friend):
#         return jsonify({'error': 'Already requested from the other user'}), 409
#
#     if friendship_service.are_friends(auth, friend):
#         return jsonify({'error': 'Already friends'}), 409
#
#     if friendship_service.has_received_request(friend, auth):
#         return jsonify(), 200
#
#     friendship_service.accept_friendship(auth, friend)
#
#     return jsonify(), 201
#
#
# @bp.route('/request/<int:id>', methods=['DELETE'])
# @auth_user(RouteType.API)
# @inject
# def delete_request(id: int,
#                    auth: User,
#                    user_repo: UserRepo = Provide[AppContainer.user_repo],
#                    friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
#     friend = user_repo.get_by_id(id)
#
#     if friend is None:
#         return jsonify({'error': f'User with {id} does not exist'}), 404
#
#     if friendship_service.is_request_pending(auth, friend):
#         friendship_service.deny_friendship(auth, friend)
#
#     return jsonify(), 200
