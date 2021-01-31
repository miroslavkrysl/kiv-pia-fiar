from flask import render_template, Flask


def register_error_handlers(app: Flask):
    app.register_error_handler(400, error400)
    app.register_error_handler(403, error403)
    app.register_error_handler(404, error404)
    app.register_error_handler(500, error500)


def error400(exception):
    return render_template('error/400.html'), 400


def error403(exception):
    return render_template('error/403.html'), 403


def error404(exception):
    return render_template('error/404.html'), 404


def error500(exception):
    return render_template('error/500.html'), 500