import os
from pathlib import Path

import rtoml
from flask import Flask

CONFIG_PATH = 'config.toml'


def load_config(app: Flask) -> dict:
    return rtoml.load(Path(app.root_path, CONFIG_PATH))


def store_config(app: Flask, config: dict):
    return rtoml.dump(config, Path(app.root_path, CONFIG_PATH), pretty=True)

