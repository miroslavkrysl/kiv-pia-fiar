from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify
from flask_socketio import emit

from fiar.data.models import User
from fiar.data.repositories.friendship import FriendshipRepo
from fiar.data.repositories.friendship_request import FriendshipRequestRepo
from fiar.data.repositories.user import UserRepo
from fiar.data.schemas import user_schema
from fiar.di.container import AppContainer
from fiar.routes.decorators import RouteType, auth_user
from fiar.routes.socket import LOBBY_NAMESPACE
from fiar.services.friendship import FriendshipService

bp = Blueprint('friendship_api', __name__)


# --- Friends ---

@bp.route('/friends', methods=['GET'])
@auth_user(RouteType.API)
@inject
def get_friends(auth: User,
                friendship_repo: FriendshipRepo = Provide[AppContainer.friendship_repo]):
    friends = friendship_repo.get_all_friends_sent_by(auth)

    return jsonify(user_schema.dump(friends, many=True))


# --- Friends requested ---

@bp.route('/friends_requested', methods=['GET'])
@auth_user(RouteType.API)
@inject
def get_friends_requested(auth: User,
                          friendship_request_repo: FriendshipRequestRepo = Provide[
                              AppContainer.friendship_request_repo]):
    users = friendship_request_repo.get_all_users_requested_by(auth)

    return jsonify(user_schema.dump(users, many=True))


# --- Friends received ---

@bp.route('/friends_received', methods=['GET'])
@auth_user(RouteType.API)
@inject
def get_friends_received(auth: User,
                         friendship_request_repo: FriendshipRequestRepo = Provide[
                             AppContainer.friendship_request_repo]):
    users = friendship_request_repo.get_all_users_received_by(auth)

    return jsonify(user_schema.dump(users, many=True))


# --- Friendship ---

@bp.route('/friendship/<int:id>', methods=['PUT'])
@auth_user(RouteType.API)
@inject
def put_friendship(id: int,
                   auth: User,
                   user_repo: UserRepo = Provide[AppContainer.user_repo],
                   friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
    friend = user_repo.get_by_id(id)

    if friend is None:
        return jsonify({'error': f'User with id {id} does not exist'}), 400
    elif friendship_service.is_request_pending(auth, friend):
        return jsonify({'error': 'Already requested'}), 400
    elif friendship_service.are_friends(auth, friend):
        return jsonify(), 200

    friendship_service.make_friendship(auth, friend)

    emit('new_request', namespace=LOBBY_NAMESPACE, to=auth.id)
    emit('new_request', namespace=LOBBY_NAMESPACE, to=friend.id)

    return jsonify(), 201

# @auth_user()
# @inject
# def delete(self,
#            id: int,
#            auth: User,
#            friendship_request_repo: FriendshipRequestRepo = Provide[Container.friendship_request_repo]):
#     req = friendship_request_repo.get_by_id(id)
#
#     if req is None:
#         return jsonify({'error': 'Request does not exist'}), 400
#     elif req.sender != auth and req.recipient != auth:
#         return jsonify({'error': 'Request is not about you'}), 403
#
#     req.delete()
#
#     emit('request_refused', namespace=LOBBY_NAMESPACE, to=req.sender.id)
#     emit('request_refused', namespace=LOBBY_NAMESPACE, to=req.recipient.id)
#
#     return jsonify(), 200
#
#
# request_api = FriendshipRequestApi.as_view('request_api')
# bp.add_url_rule('/request/', view_func=request_api, methods=['POST'])
# bp.add_url_rule('/api/request/<int:id>', view_func=request_api, methods=['DELETE'])
#
#
# class FriendshipApi(MethodView):
#     @auth_user()
#     @inject
#     def post(self,
#              auth: User,
#              user_repo: UserRepo = Provide[Container.user_repo],
#              friendship_repo: FriendshipRepo = Provide[Container.friendship_repo],
#              friendship_request_repo: FriendshipRequestRepo = Provide[Container.friendship_request_repo]):
#         try:
#             data = id_schema.load(request.form)
#         except ValidationError as err:
#             return jsonify({"errors": err.messages}), 400
#
#         errors = {}
#         error = None
#
#         friend = user_repo.get_by_id(data['id'])
#
#         if friend is None:
#             errors['id'] = ['User does not exist']
#         else:
#             req = friendship_request_repo.get_by_users(friend, auth)
#
#         if friendship_repo.get_by_users(auth, friend) is not None:
#             error = 'Already friends'
#         elif request is None:
#             error = 'Friendship not requested'
#
#         if errors:
#             return jsonify({'errors': errors}), 400
#         elif error:
#             return jsonify({'error': error}), 400
#
#         req.delete()
#         friendship_repo.create(auth, friend)
#
#         emit('new_friend', namespace=LOBBY_NAMESPACE, to=friend.id)
#         emit('new_friend', namespace=LOBBY_NAMESPACE, to=auth.id)
#
#         return jsonify(), 201
#
#     @auth_user()
#     @inject
#     def delete(self,
#                id: int,
#                auth: User,
#                friendship_repo: FriendshipRepo = Provide[Container.friendship_repo]):
#         fs = friendship_repo.get_by_id(id)
#
#         if fs is None:
#             return jsonify({'error': 'Friendship does not exist'}), 400
#         elif fs.sender != auth and fs.recipient != auth:
#             return jsonify({'error': 'Friendship is not about you'}), 403
#
#         fs.delete()
#
#         emit('friend_removed', namespace=LOBBY_NAMESPACE, to=fs.sender.id)
#         emit('friend_removed', namespace=LOBBY_NAMESPACE, to=fs.recipient.id)
#
#         return jsonify(), 200
#
#
# friendship_api = FriendshipApi.as_view('friendship_api')
# bp.add_url_rule('/api/friendship/', view_func=friendship_api, methods=['POST'])
# bp.add_url_rule('/api/friendship/<int:id>', view_func=friendship_api, methods=['DELETE'])
#
#
#
#
# @bp.route('/ajax/friends_rows')
# @auth_user()
# @inject
# def friends_rows(auth: User,
#                  friendship_repo: FriendshipRepo = Provide[Container.friendship_repo]):
#     friendships = friendship_repo.get_all_of(auth)
#     return render_template('ajax/friends_rows.html', friendships=friendships)
#
#
# @bp.route('/ajax/friendship_requests_rows')
# @auth_user()
# @inject
# def friendship_requests_rows(auth: User,
#                              friendship_request_repo: FriendshipRequestRepo = Provide[
#                                  Container.friendship_request_repo]):
#     requests = friendship_request_repo.get_all_of(auth)
#     return render_template('ajax/friendship_requests_rows.html', requests=requests)
