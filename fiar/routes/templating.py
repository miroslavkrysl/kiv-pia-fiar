from dependency_injector.wiring import inject, Provide
from flask import Flask

from fiar.di.container import AppContainer
from fiar.services.auth import AuthService


def register_preprocessors(app: Flask):
    app.context_processor(inject_auth_user)


# --- Preprocessors ---

@inject
def inject_auth_user(auth_service: AuthService = Provide[AppContainer.auth_service]):
    """
    g.auth_user
    """
    return dict(auth_user=auth_service.get_user())
