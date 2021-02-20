from flask import Flask

from fiar.routes.api import user, friendship

API_PREFIX = '/api'


def register_api_routes(app: Flask):
    app.register_blueprint(user.bp, url_prefix=API_PREFIX + '/user')
    app.register_blueprint(friendship.bp, url_prefix=API_PREFIX + '/friendship')
