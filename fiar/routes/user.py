from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, Request, g, redirect, url_for, jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields, validate, pre_load, ValidationError

from fiar.di import Container
from fiar.schemas import user_login_schema
from fiar.services.auth import AuthService

bp = Blueprint('user', __name__)

# --- HTML ---

@bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET'])
@inject
def register():
    return render_template('auth/register.html')


# --- REST ---

class LoginSchema(Schema):
    email = fields.Email(required=True, validate=[
        validate.Length
    ])
    password = fields.Str(required=True)

    @pre_load
    def process_input(self, data, **kwargs):
        data["email"] = data["email"].lower().strip()
        return data


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
            return jsonify({"error": "Wrong email or password"}), 401

        auth_service.login(user)
        return jsonify(), 201

    @inject
    def delete(self,
               auth_service: AuthService = Provide[Container.auth_service]):
        if auth_service.get_user() is None:
            return jsonify({"error": "Not logged in"}), 404

        auth_service.logout()
        return jsonify(), 200


bp.add_url_rule('/api/login', view_func=LoginApi.as_view('login_api'))
