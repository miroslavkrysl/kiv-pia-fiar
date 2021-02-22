from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, abort

from fiar.data.models import User
from fiar.di.container import AppContainer
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.routes.decorators import RouteType, auth_user, admin_only
from fiar.services.pswd_token import PswdTokenService

bp = Blueprint('user', __name__)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('user/login.html')


@bp.route('/registration', methods=['GET'])
def registration():
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


@bp.route('/profile', methods=['GET'])
@auth_user(RouteType.HTML)
def profile(auth: User):
    return render_template('user/profile.html', user=auth)


@bp.route('/profile/<int:id>', methods=['GET'])
@auth_user(RouteType.HTML)
@admin_only(RouteType.HTML)
@inject
def foreign_profile(id: int,
                    user_repo: UserRepo = Provide[AppContainer.user_repo]):
    user = user_repo.get_by_id(id)

    if user is None:
        abort(404, description=f"User with id {id} does not exist")

    return render_template('user/profile.html', user=user)


@bp.route('/administration', methods=['GET'])
@auth_user(RouteType.HTML)
@admin_only(RouteType.HTML)
@inject
def administration(user_repo: UserRepo = Provide[AppContainer.user_repo]):
    users = user_repo.get_all(order_by=UserRepo.OrderBy.USERNAME)
    return render_template('user/administration.html', users=users)
