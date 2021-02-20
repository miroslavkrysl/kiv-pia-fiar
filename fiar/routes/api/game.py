from flask import Blueprint

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

# @bp.route('/friendship/<int:id>', methods=['PUT'])
# @auth_user(RouteType.API)
# @inject
# def put_friendship(id: int,
#                    auth: User,
#                    user_repo: UserRepo = Provide[AppContainer.user_repo],
#                    friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
#     friend = user_repo.get_by_id(id)
#
#     if friend is None:
#         return jsonify({'error': f'User with id {id} does not exist'}), 400
#
#     if friendship_service.are_friends(auth, friend):
#         return jsonify(), 200
#
#     if not friendship_service.has_received_request(auth, friend):
#         return jsonify({'error': 'Friendship not requested from the other user.'}), 409
#
#     friendship_service.accept_friendship(auth, friend)
#
#     return jsonify(), 201
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
