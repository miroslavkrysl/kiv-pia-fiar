from functools import wraps

from dependency_injector.wiring import inject, Provide
from flask import url_for, redirect, g, request, jsonify, abort

from fiar.di import Container
from fiar.services.auth import AuthService


def auth_required(f):
    @inject
    def _auth_required(auth_service: AuthService = Provide[Container.auth_service]):
        if auth_service.get_user() is None:
            return redirect(url_for('user.login'))

        return None

    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = _auth_required()

        if result is not None:
            return result

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @inject
    def _admin_required():
        if g.auth_user is None or not g.auth_user.is_admin:
            description = "You must be an admin to access this area"

            if request.content_type == 'application/json':
                return jsonify(error=description), 403

            abort(403, description=description)

        return None

    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = _admin_required()

        if result is not None:
            return result

        return f(*args, **kwargs)

    return decorated_function
