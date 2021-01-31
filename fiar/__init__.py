import sys

from fiar import controllers, persistence, services
from fiar.app import create_app
from fiar.di import Container, create_container

# create app and app di container
app = create_app()
container = create_container(app)

packages = [
    controllers,
    persistence,
    services
]

# wire all di dependencies
container.wire(packages=packages)
