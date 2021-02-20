from flask import Flask

from fiar.routes.html import user
from fiar.routes.html import lobby


def register_html_routes(app: Flask):
    app.register_blueprint(lobby.bp, url_prefix='/')
    app.register_blueprint(user.bp, url_prefix='/user')
