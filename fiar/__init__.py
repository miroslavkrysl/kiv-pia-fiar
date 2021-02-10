import sys

from fiar.app import create_app
from fiar.di import create_container

# create app and app di container
app = create_app()
container = create_container(app, __name__)