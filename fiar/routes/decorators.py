from functools import wraps

from dependency_injector.wiring import inject, Provide
from flask import url_for, redirect

from fiar.di import Container
from fiar.services.auth import AuthService


@inject
def _auth_required(*args, _auth_service_: AuthService = Provide[Container.auth_service], **kwargs):
    if _auth_service_.get_user() is None:
        return redirect(url_for('auth.login'))

    return None


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = _auth_required()

        if result is not None:
            return result

        return f(*args, **kwargs)

    return decorated_function
