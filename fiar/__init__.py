from fiar.app import create_app

# create app and app di container
from fiar.di.container import init_container

app = create_app()
init_container(app)
