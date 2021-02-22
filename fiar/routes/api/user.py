from datetime import timedelta

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, jsonify, request, url_for, render_template
from marshmallow import fields, ValidationError

from fiar.data.models import User
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.data.schemas import UserSchema, user_schema, admin_schema
from fiar.di.container import AppContainer
from fiar.routes.decorators import RouteType, auth_user, admin_only
from fiar.services.auth import AuthService
from fiar.services.friendship import FriendshipService
from fiar.services.game import GameService
from fiar.services.mail import MailService
from fiar.services.pswd_token import PswdTokenService
from fiar.services.user import UserService

bp = Blueprint('user_api', __name__)


# --- User ---

class UserWithInviteSchema(UserSchema):
    has_sent_invite = fields.Boolean()


user_with_invite_schema = UserWithInviteSchema()


@bp.route('/user/<int:id>', methods=['GET'])
@auth_user(RouteType.API)
@inject
def get_user(auth: User,
             id: int,
             user_repo: UserRepo = Provide[AppContainer.user_repo],
             game_service: GameService = Provide[AppContainer.game_service]):
    user = user_repo.get_by_id(id)

    if user is None:
        return jsonify({'error': f'User with id {id} does not exist'}), 404

    user.has_sent_invite = game_service.has_received_invite(auth, user)

    return jsonify(user_with_invite_schema.dump(user))


# --- Registration ---

@bp.route('/registration', methods=['POST'])
@inject
def post_registration(auth_service: AuthService = Provide[AppContainer.auth_service],
                      user_service: UserService = Provide[AppContainer.user_service]):
    try:
        data = user_schema.load(request.form)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    errors = {}

    if user_service.username_exists(data['username']):
        errors['username'] = ['Already taken']
    if user_service.email_exists(data['email']):
        errors['email'] = ['Already taken']

    if errors:
        return jsonify({"errors": errors}), 400

    user = user_service.create_user(**data)
    auth_service.login(user)

    return jsonify(user_schema.dump(user)), 201


# --- Login ---

login_schema = UserSchema(only=['email', 'password'])


@bp.route('/login', methods=['PUT'])
@inject
def put_login(auth_service: AuthService = Provide[AppContainer.auth_service]):
    try:
        data = login_schema.load(request.form)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = auth_service.auth_email_password(**data)

    if user is None:
        return jsonify({"error": "Wrong email or password"}), 400

    auth_service.login(user)
    return jsonify(), 201


@bp.route('/login', methods=['DELETE'])
@inject
def delete_login(auth_service: AuthService = Provide[AppContainer.auth_service]):
    if auth_service.get_user() is None:
        return jsonify({"error": "Not logged in"}), 404

    auth_service.logout()
    return jsonify(), 200


# --- Pswd reset email ---

email_schema = UserSchema(only=['email'])


@bp.route('/pswd-reset-email', methods=['POST'])
@inject
def post_pswd_reset_email(user_repo: UserRepo = Provide[AppContainer.user_repo],
                          pswd_token_service: PswdTokenService = Provide[AppContainer.pswd_token_service],
                          mail_service: MailService = Provide[AppContainer.mail_service]):
    try:
        data = email_schema.load(request.form)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = user_repo.get_by_email(data['email'])

    if user:
        token = pswd_token_service.make_token(user)
        url = url_for('user.password_reset', token=token, _external=True)
        mail_service.send('Password reset', user.email, render_template('mail/pswd_reset.html', url=url))

    return jsonify(), 202


# --- Pswd reset ---

pswd_schema = UserSchema(only=['password'])


@bp.route('/pswd-reset/<token>', methods=['PUT'])
@inject
def put_pswd_reset(token: str,
                   user_service: UserService = Provide[AppContainer.user_service],
                   pswd_reset_service: PswdTokenService = Provide[AppContainer.pswd_token_service]):
    try:
        data = pswd_schema.load(request.form)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = pswd_reset_service.decode_token(token)

    if user is None:
        return jsonify({"error": "Expired or invalid password reset token"}), 400

    user_service.change_password(user, data['password'])
    user_service.change_uid(user)

    return jsonify(), 200


# --- Pswd change ---

@bp.route('/pswd-change/<int:id>', methods=['PUT'])
@auth_user(RouteType.API)
@inject
def put_pswd_change(id: int,
                    auth: User,
                    user_service: UserService = Provide[AppContainer.user_service],
                    user_repo: UserRepo = Provide[AppContainer.user_repo],
                    auth_service: AuthService = Provide[AppContainer.auth_service]):
    user = user_repo.get_by_id(id)

    if user is None:
        return jsonify({"error": f"User with id {id} does not exist"}), 404

    try:
        data = pswd_schema.load(request.form)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user_service.change_password(user, data['password'])
    user_service.change_uid(user)
    auth_service.login(user)

    return jsonify(), 200


# --- Admin ---

@bp.route('/admin/<int:id>', methods=['PUT'])
@auth_user(RouteType.API)
@admin_only(RouteType.API)
@inject
def put_admin(id: int,
              user_repo: UserRepo = Provide[AppContainer.user_repo]):
    user = user_repo.get_by_id(id)

    if user is None:
        return jsonify({"error": f"User with id {id} does not exist"}), 404

    try:
        data = admin_schema.load(request.form)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user.is_admin = data['is_admin']
    return jsonify(), 200
