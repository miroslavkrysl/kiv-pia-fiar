from flask import render_template, Flask, request
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask):
    app.register_error_handler(HTTPException, http_exception)


def http_exception(exception: HTTPException, **kwargs):
    return render_template('error.html',
                           description=exception.description,
                           name=exception.name,
                           code=exception.code)
