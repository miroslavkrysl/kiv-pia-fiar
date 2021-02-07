import os
from functools import wraps
from pathlib import Path
from threading import Thread

import rtoml
from flask import Flask

CONFIG_PATH = 'config.toml'


def load_config(app: Flask) -> dict:
    return rtoml.load(Path(app.root_path, CONFIG_PATH))


def store_config(app: Flask, config: dict):
    return rtoml.dump(config, Path(app.root_path, CONFIG_PATH), pretty=True)


def async_task(f):
    """ Takes a function and runs it in a thread """

    @wraps(f)
    def _decorated(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return _decorated
