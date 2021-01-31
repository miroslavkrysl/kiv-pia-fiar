import sys

from fiar.app import create_app
from fiar.di import Container, create_container

# create app and app di container
app = create_app()
container = create_container(app)


# wire all di dependencies
container.wire(packages=[sys.modules[__name__]])
