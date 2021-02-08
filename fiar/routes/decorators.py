from functools import wraps

from dependency_injector.wiring import inject, Provide
from flask import url_for, redirect, g, request, jsonify, abort
from flask_socketio import disconnect

from fiar.db import Db
from fiar.di import Container
from fiar.services.auth import AuthService


@inject
def _authenticated_user(auth_service: AuthService = Provide[Container.auth_service]):
    """Get the authenticated user."""
    return auth_service.get_user()


@inject
def _is_admin(auth_service: AuthService = Provide[Container.auth_service]):
    """Check if authenticated user is admin"""
    return auth_service.get_user().is_admin


def auth_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = _authenticated_user()
        if user is None:
            return redirect(url_for('user.login'))
        else:
            return f(*args, auth_user=user, **kwargs)

    return decorated_function


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not _is_admin():
            description = "You must be an admin to access this area"
            abort(403, description=description)

        return f(*args, **kwargs)

    return decorated_function


def socket_context(f):
    @inject
    def _before(database: Db = Provide[Container.db],
                auth_service: AuthService = Provide[Container.auth_service]):
        database.enter_session()
        auth_service.load_user()

    @inject
    def _after(database: Db = Provide[Container.db]):
        database.exit_session()

    @wraps(f)
    def decorated_function(*args, **kwargs):
        _before()
        f(*args, **kwargs)
        _after()

    return decorated_function


def socket_auth_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = _authenticated_user()
        if user is None:
            disconnect()
        else:
            return f(*args, auth_user=user, **kwargs)

    return decorated_function
