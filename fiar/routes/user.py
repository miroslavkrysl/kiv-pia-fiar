from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError

from fiar.di import Container
from fiar.repositories.user import UserRepo
from fiar.schemas import user_login_schema, user_schema
from fiar.services.auth import AuthService

bp = Blueprint('user', __name__)


# --- HTML ---

@bp.route('/login', methods=['GET'])
def login():
    return render_template('user/login.html')


@bp.route('/register', methods=['GET'])
@inject
def register():
    return render_template('user/register.html')


# --- REST ---

class RegisterApi(MethodView):
    @inject
    def post(self,
             auth_service: AuthService = Provide[Container.auth_service],
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

        user = user_repo.create(**data)
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


bp.add_url_rule('/api/register', view_func=RegisterApi.as_view('register_api'))
bp.add_url_rule('/api/login', view_func=LoginApi.as_view('login_api'))
