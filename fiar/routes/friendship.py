from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_socketio import emit
from marshmallow import ValidationError

from fiar.db import User
from fiar.di import Container
from fiar.repositories.friendship import FriendshipRepo
from fiar.repositories.friendship_request import FriendshipRequestRepo
from fiar.repositories.user import UserRepo
from fiar.routes import LOBBY_NAMESPACE
from fiar.routes.decorators import auth_user
from fiar.schemas import id_schema

bp = Blueprint('friendship', __name__)


# --- REST ---

class FriendshipRequestApi(MethodView):
    @auth_user()
    @inject
    def post(self,
             auth: User,
             user_repo: UserRepo = Provide[Container.user_repo],
             friendship_repo: FriendshipRepo = Provide[Container.friendship_repo],
             friendship_request_repo: FriendshipRequestRepo = Provide[Container.friendship_request_repo]):
        try:
            data = id_schema.load(request.form)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        errors = {}
        error = None

        friend = user_repo.get_by_id(data['id'])

        if friend is None:
            errors['id'] = ['User does not exist']
        elif friendship_request_repo.get_by_users(auth, friend) is not None:
            error = 'Already requested'
        elif friendship_repo.get_by_users(auth, friend) is not None:
            error = 'Already friends'

        if errors:
            return jsonify({'errors': errors}), 400
        elif error:
            return jsonify({'error': error}), 400

        friendship_request_repo.create(auth, friend)

        emit('new_request', namespace=LOBBY_NAMESPACE, to=auth.id)
        emit('new_request', namespace=LOBBY_NAMESPACE, to=friend.id)

        return jsonify(), 201

    @auth_user()
    @inject
    def delete(self,
               id: int,
               auth: User,
               friendship_request_repo: FriendshipRequestRepo = Provide[Container.friendship_request_repo]):

        req = friendship_request_repo.get_by_id(id)

        if req is None:
            return jsonify({'error': 'Request does not exist'}), 400
        elif req.sender != auth and req.recipient != auth:
            return jsonify({'error': 'Request is not about you'}), 403

        req.delete()

        emit('request_refused', namespace=LOBBY_NAMESPACE, to=req.sender.id)
        emit('request_refused', namespace=LOBBY_NAMESPACE, to=req.recipient.id)

        return jsonify(), 200


request_api = FriendshipRequestApi.as_view('request_api')
bp.add_url_rule('/api/request/', view_func=request_api, methods=['POST'])
bp.add_url_rule('/api/request/<int:id>', view_func=request_api, methods=['DELETE'])


class FriendshipApi(MethodView):
    @auth_user()
    @inject
    def post(self,
             auth: User,
             user_repo: UserRepo = Provide[Container.user_repo],
             friendship_repo: FriendshipRepo = Provide[Container.friendship_repo],
             friendship_request_repo: FriendshipRequestRepo = Provide[Container.friendship_request_repo]):
        try:
            data = id_schema.load(request.form)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        errors = {}
        error = None

        friend = user_repo.get_by_id(data['id'])

        if friend is None:
            errors['id'] = ['User does not exist']
        else:
            req = friendship_request_repo.get_by_users(friend, auth)

        if friendship_repo.get_by_users(auth, friend) is not None:
            error = 'Already friends'
        elif request is None:
            error = 'Friendship not requested'

        if errors:
            return jsonify({'errors': errors}), 400
        elif error:
            return jsonify({'error': error}), 400

        req.delete()
        friendship_repo.create(auth, friend)

        emit('new_friend', namespace=LOBBY_NAMESPACE, to=friend.id)
        emit('new_friend', namespace=LOBBY_NAMESPACE, to=auth.id)

        return jsonify(), 201

    @auth_user()
    @inject
    def delete(self,
               id: int,
               auth: User,
               friendship_repo: FriendshipRepo = Provide[Container.friendship_repo]):
        fs = friendship_repo.get_by_id(id)

        if fs is None:
            return jsonify({'error': 'Friendship does not exist'}), 400
        elif fs.sender != auth and fs.recipient != auth:
            return jsonify({'error': 'Friendship is not about you'}), 403

        fs.delete()

        emit('friend_removed', namespace=LOBBY_NAMESPACE, to=fs.sender.id)
        emit('friend_removed', namespace=LOBBY_NAMESPACE, to=fs.recipient.id)

        return jsonify(), 200


friendship_api = FriendshipApi.as_view('friendship_api')
bp.add_url_rule('/api/friendship/', view_func=friendship_api, methods=['POST'])
bp.add_url_rule('/api/friendship/<int:id>', view_func=friendship_api, methods=['DELETE'])
