from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, abort

from fiar.di.container import AppContainer
from fiar.services.pswd_token import PswdTokenService

bp = Blueprint('user', __name__)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('user/login.html')


@bp.route('/register', methods=['GET'])
def register():
    return render_template('user/registration.html')


@bp.route('/forgotten_password', methods=['GET'])
def forgot_password():
    return render_template('user/forgotten_password.html')


@bp.route('/password_reset/<token>', methods=['GET'])
@inject
def password_reset(token: str,
                   pswd_reset_service: PswdTokenService = Provide[AppContainer.pswd_token_service]):
    user = pswd_reset_service.decode_token(token)

    if user is not None:
        return render_template('user/password_reset.html', token=token)
    else:
        abort(401, description="Expired or invalid password reset token")
