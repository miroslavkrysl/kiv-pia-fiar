from enum import Enum, auto
from functools import wraps

import wrapt
import inspect

from dependency_injector.wiring import inject, Provide
from flask import url_for, redirect, abort, jsonify
from flask_socketio import disconnect

from fiar.di.container import AppContainer
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.services.auth import AuthService


class RouteType(Enum):
    HTML = auto()
    API = auto()
    SOCKET = auto()


# --- Helpers ---

@inject
def _authenticated_user(auth_service: AuthService = Provide[AppContainer.auth_service]):
    """Get the authenticated user."""
    return auth_service.get_user()


@inject
def _is_admin(auth_service: AuthService = Provide[AppContainer.auth_service]):
    """Check if authenticated user is admin"""
    return auth_service.get_user().is_admin


# --- Decorators ---

def auth_user(route_type: RouteType, require_auth: bool = True):
    """
    Load authenticated user and inject him into the 'auth' argument,
    or inject None if not authenticated.
    :param route_type: Type of the route.
    :param require_auth: If set to True and the user is not authenticated,
    returns redirect response to login page.
    :return: Decorator function.
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        user = _authenticated_user()

        if user is None and require_auth:
            if route_type == RouteType.HTML:
                return redirect(url_for('user.login'))
            if route_type == RouteType.API:
                return jsonify(401)
            if route_type == RouteType.SOCKET:
                disconnect()
        else:
            if 'auth' in inspect.signature(wrapped).parameters:
                return wrapped(*args, auth=user, **kwargs)
            else:
                return wrapped(*args, **kwargs)

    return wrapper


def admin_only(route_type: RouteType):
    """
    Load authenticated user and require that he is an admin.
    :param route_type: Type of the route.
    :return: Decorator function.
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        if not _is_admin():
            description = "You must be an admin to access this area"

            if route_type == RouteType.HTML:
                abort(403, description=description)
            if route_type == RouteType.API:
                return jsonify(403, {'error': description})
            if route_type == RouteType.SOCKET:
                disconnect()

        return wrapped(*args, **kwargs)

    return wrapper


def socket_context():
    """
    Manually trigger necessary request before/after actions.
    It is needed, because socket request does not trigger them
    automatically.
    :return: Decorator function.
    """

    @inject
    def _after(database: SqlAlchemyDb = Provide[AppContainer.sqlalchemy_db]):
        database.exit_session()

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        wrapped(*args, **kwargs)
        _after()

    return wrapper
