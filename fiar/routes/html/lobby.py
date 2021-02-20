from flask import Blueprint, render_template

from fiar.data.models import User
from fiar.routes.decorators import auth_user, RouteType

bp = Blueprint('lobby', __name__)


@bp.route('/')
@auth_user(RouteType.HTML, False)
def index(auth: User):
    if auth:
        return render_template('lobby.html')
    else:
        return render_template('index.html')
