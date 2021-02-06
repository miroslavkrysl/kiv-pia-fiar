from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template

from fiar.di import Container
from fiar.services.auth import AuthService

bp = Blueprint('lobby', __name__)


@bp.route('/')
@inject
def index(auth_service: AuthService = Provide[Container.auth_service]):
    if auth_service.is_authenticated():
        return render_template('lobby.html')
    else:
        return render_template('index.html')
