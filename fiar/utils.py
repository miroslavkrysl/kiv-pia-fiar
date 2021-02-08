from functools import wraps
from pathlib import Path
from threading import Thread

import rtoml
from flask import Flask, current_app

CONFIG_PATH = 'config.toml'


def load_config(app: Flask) -> dict:
    """
    Load config from predefined toml file.
    :param app: App instance.
    :return: Dict with config values.
    """
    return rtoml.load(Path(app.root_path, CONFIG_PATH))


def store_config(app: Flask, config: dict):
    """
    Store config into predefined toml file.
    :param app: App instance.
    :param config: Dict with config values.
    """
    return rtoml.dump(config, Path(app.root_path, CONFIG_PATH), pretty=True)


def async_task(f):
    """
    Modifies a function to run it in a thread.
    """

    @wraps(f)
    def _decorated(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return _decorated


def with_request_context(f):
    """
    Modifies a function to run it inside a dummy request context.
    """

    @wraps(f)
    def _decorated(*args, **kwargs):
        ctx = current_app.test_request_context()
        ctx.push()
        current_app.preprocess_request()

        f(*args, **kwargs)

        ctx.pop()

    return _decorated
