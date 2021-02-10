from functools import partial, wraps

import wrapt
import inspect

from dependency_injector.wiring import inject, Provide
from flask import url_for, redirect, abort
from flask_socketio import disconnect

from fiar.di import Container
from fiar.services.db import Db
from fiar.services.auth import AuthService


@inject
def _authenticated_user(auth_service: AuthService = Provide[Container.auth_service]):
    """Get the authenticated user."""
    return auth_service.get_user()


@inject
def _is_admin(auth_service: AuthService = Provide[Container.auth_service]):
    """Check if authenticated user is admin"""
    return auth_service.get_user().is_admin


def auth_user(require_auth=True):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        user = _authenticated_user()

        if user is None and require_auth:
            return redirect(url_for('user.login'))
        else:
            if 'auth' in inspect.signature(wrapped).parameters:
                return wrapped(*args, auth=user, **kwargs)
            else:
                return wrapped(*args, **kwargs)

    return wrapper


def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not _is_admin():
            description = "You must be an admin to access this area"
            abort(403, description=description)

        return f(*args, **kwargs)

    return wrapper


def socket_context(f):
    @inject
    def _before(database: Db = Provide[Container.db],
                auth_service: AuthService = Provide[Container.auth_service]):
        database.enter_session()
        auth_service.load_user()

    @inject
    def _after(database: Db = Provide[Container.db]):
        database.exit_session()

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        _before()
        wrapped(*args, **kwargs)
        _after()

    return wrapper(f)


def socket_auth_user(require_auth=True):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        user = _authenticated_user()

        if user is None and require_auth:
            disconnect()
        else:
            if 'auth' in inspect.signature(wrapped).parameters:
                wrapped(*args, auth=user, **kwargs)
            else:
                wrapped(*args, **kwargs)

    return wrapper
