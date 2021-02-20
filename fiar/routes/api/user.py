from datetime import timedelta

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, jsonify
from marshmallow import fields

from fiar.data.models import User
from fiar.data.repositories.user import UserRepo
from fiar.data.schemas import UserSchema
from fiar.di.container import AppContainer
from fiar.routes.decorators import RouteType, auth_user
from fiar.services.friendship import FriendshipService

bp = Blueprint('user_api', __name__)


class UserWithFriendshipSchema(UserSchema):
    is_friend = fields.Boolean()
    is_request_pending = fields.Boolean()


user_with_friendship_schema = UserWithFriendshipSchema()


@bp.route('/online-users', methods=['GET'])
@auth_user(RouteType.API)
@inject
def get_online_users(auth: User,
                     user_repo: UserRepo = Provide[AppContainer.user_repo],
                     friendship_service: FriendshipService = Provide[AppContainer.friendship_service]):
    users = user_repo.get_all_online(timedelta(seconds=current_app.config['USER']['ONLINE_TIMEOUT']))

    for user in users:
        user.is_friend = friendship_service.are_friends(auth, user)
        user.is_request_pending = friendship_service.is_request_pending(auth, user)

    return jsonify(user_with_friendship_schema.dump(users, many=True))
