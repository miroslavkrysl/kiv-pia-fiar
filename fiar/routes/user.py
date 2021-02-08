from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, jsonify, request, abort, url_for
from flask.views import MethodView
from flask_socketio import Namespace
from marshmallow import ValidationError

from fiar.db import User
from fiar.di import Container
from fiar.repositories.user import UserRepo
from fiar.routes.decorators import socket_auth_user, socket_context
from fiar.schemas import user_login_schema, user_schema, user_pswd_reset_schema, user_pswd_reset_email_schema
from fiar.services.auth import AuthService
from fiar.services.mail import MailService
from fiar.services.pswd_reset import PswdResetService
from fiar.services.user import UserService

bp = Blueprint('user', __name__)


# --- HTML ---

@bp.route('/login', methods=['GET'])
def login():
    return render_template('user/login.html')


@bp.route('/register', methods=['GET'])
@inject
def register():
    return render_template('user/register.html')


@bp.route('/forgot_password', methods=['GET'])
@inject
def forgot_password():
    return render_template('user/forgot_password.html')


@bp.route('/password_reset/<token>', methods=['GET'])
@inject
def password_reset(token: str,
                   pswd_reset_service: PswdResetService = Provide[Container.pswd_reset_service]):
    user = pswd_reset_service.decode_reset_token(token)

    if user is not None:
        return render_template('user/password_reset.html', token=token)
    else:
        abort(401, description="Expired or invalid password reset token")


# --- Socket ---

class UserSocket(Namespace):
    def on_connect(self):
        print('connected')

    def on_disconnect(self):
        print('disconnected')

    @socket_context
    @socket_auth_user
    @inject
    def on_active(self,
                  data,
                  auth_user: User,
                  user_service: UserService = Provide[Container.user_service]):
        user_service.update_last_active_at(auth_user)


# --- REST ---

class RegisterApi(MethodView):
    @inject
    def post(self,
             auth_service: AuthService = Provide[Container.auth_service],
             user_service: UserService = Provide[Container.user_service],
             user_repo: UserRepo = Provide[Container.user_repo]):
        try:
            data = user_schema.load(request.form)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        errors = {}

        if user_repo.get_by_username(data['username']) is not None:
            errors['username'] = ['Username is already taken']
        if user_repo.get_by_email(data['email']) is not None:
            errors['email'] = ['Email is already taken']

        if errors:
            return jsonify({"errors": errors}), 400

        user = user_service.create_user(**data)
        auth_service.login(user)

        return jsonify(user_schema.dump(user)), 201


class LoginApi(MethodView):
    @inject
    def post(self,
             auth_service: AuthService = Provide[Container.auth_service]):
        try:
            data = user_login_schema.load(request.form)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        user = auth_service.auth_email_password(**data)

        if user is None:
            return jsonify({"error": "Wrong email or password"}), 400

        auth_service.login(user)
        return jsonify(), 201

    @inject
    def delete(self,
               auth_service: AuthService = Provide[Container.auth_service]):
        if auth_service.get_user() is None:
            return jsonify({"error": "Not logged in"}), 404

        auth_service.logout()
        return jsonify(), 200


class PswdResetEmailApi(MethodView):
    @inject
    def post(self,
             user_repo: UserRepo = Provide[Container.user_repo],
             pswd_reset_service: PswdResetService = Provide[Container.pswd_reset_service],
             mail_service: MailService = Provide[Container.mail_service]):
        try:
            data = user_pswd_reset_email_schema.load(request.form)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        user = user_repo.get_by_email(data['email'])

        if user is None:
            return jsonify({"errors": {"email": ["Email does not exist"]}}), 400

        token = pswd_reset_service.make_reset_token(user)
        url = url_for('user.password_reset', token=token, _external=True)
        mail_service.send("Password reset", user.email, render_template('mail/pswd_reset.html', url=url))

        return jsonify(), 201


class PswdResetApi(MethodView):
    @inject
    def put(self,
            token: str,
            user_service: UserService = Provide[Container.user_service],
            pswd_reset_service: PswdResetService = Provide[Container.pswd_reset_service]):
        try:
            data = user_pswd_reset_schema.load(request.form)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        user = pswd_reset_service.decode_reset_token(token)

        if user is None:
            return jsonify({"error": "Expired or invalid password reset token"}), 400

        user_service.change_password(user, data['password'])
        user_service.change_uid(user)

        return jsonify(), 200


bp.add_url_rule('/api/register', view_func=RegisterApi.as_view('register_api'))
bp.add_url_rule('/api/login', view_func=LoginApi.as_view('login_api'))
bp.add_url_rule('/api/password_reset/<token>', view_func=PswdResetApi.as_view('password_reset_api'))
bp.add_url_rule('/api/password_reset_send', view_func=PswdResetEmailApi.as_view('password_reset_email_api'))
