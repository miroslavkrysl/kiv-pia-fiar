from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify

from fiar.data.models import User
from fiar.persistence.sqlalchemy.repositories.friendship import FriendshipRepo
from fiar.persistence.sqlalchemy.repositories.request import RequestRepo
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.data.schemas import friendship_schema, request_schema
from fiar.di.container import AppContainer
from fiar.routes.decorators import RouteType, auth_user
from fiar.services.friendship import FriendshipService

bp = Blueprint('friendship_api', __name__)


# --- Friendships ---

@bp.route('/friendships', methods=['GET'])
@auth_user(RouteType.API)
@inject
def get_friendships(auth: User,
                friendship_repo: FriendshipRepo = Provide[AppContainer.friendship_repo]):
    friendships = friendship_repo.get_all_by_user(auth)
    return jsonify(friendship_schema.dump(friendships, many=True))


# --- Friendship requests ---

@bp.route('/requests', methods=['GET'])
@auth_user(RouteType.API)
@inject
def get_requests(auth: User,
                 request_repo: RequestRepo = Provide[AppContainer.request_repo]):
    requests = request_repo.get_all_by_user(auth)
    return jsonify(request_schema.dump(requests, many=True))


# --- Friendship ---

@bp.route('/friendship/<int:friend_id>', methods=['PUT'])
@auth_user(RouteType.API)
@inject
def put_friendship(friend_id: int,
                   auth: User,
                   user_repo: UserRepo = Provide[AppContainer.user_repo],
                   friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
    friend = user_repo.get_by_id(friend_id)

    if friend is None:
        return jsonify({'error': f'User with id {friend_id} does not exist'}), 404

    if friendship_service.are_friends(auth, friend):
        return jsonify(), 200

    if not friendship_service.has_received_request(auth, friend):
        return jsonify({'error': 'Friendship not requested from the other user.'}), 409

    friendship_service.accept_friendship(auth, friend)

    return jsonify(), 201


@bp.route('/friendship/<int:friend_id>', methods=['DELETE'])
@auth_user(RouteType.API)
@inject
def delete_friendship(friend_id: int,
                      auth: User,
                      user_repo: UserRepo = Provide[AppContainer.user_repo],
                      friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
    friend = user_repo.get_by_id(friend_id)

    if friend is None:
        return jsonify({'error': f'User with {friend_id} does not exist'}), 404

    if friendship_service.are_friends(auth, friend):
        friendship_service.remove_friendship(auth, friend)

    return jsonify(), 200


# --- Friendship request ---

@bp.route('/request/<int:friend_id>', methods=['POST'])
@auth_user(RouteType.API)
@inject
def post_request(friend_id: int,
                 auth: User,
                 user_repo: UserRepo = Provide[AppContainer.user_repo],
                 friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
    friend = user_repo.get_by_id(friend_id)

    if friend is None:
        return jsonify({'error': f'User with id {friend_id} does not exist'}), 404

    if friendship_service.has_received_request(auth, friend):
        return jsonify({'error': 'Already requested from the other user'}), 409

    if friendship_service.are_friends(auth, friend):
        return jsonify({'error': 'Already friends'}), 409

    if friendship_service.has_received_request(friend, auth):
        return jsonify(), 200

    friendship_service.create_request(auth, friend)

    return jsonify(), 201


@bp.route('/request/<int:friend_id>', methods=['DELETE'])
@auth_user(RouteType.API)
@inject
def delete_request(friend_id: int,
                   auth: User,
                   user_repo: UserRepo = Provide[AppContainer.user_repo],
                   friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
    friend = user_repo.get_by_id(friend_id)

    if friend is None:
        return jsonify({'error': f'User with {friend_id} does not exist'}), 404

    if friendship_service.is_request_pending(auth, friend):
        friendship_service.remove_pending_requests(auth, friend)

    return jsonify(), 200
