from fiar import app, container

if __name__ == '__main__':
    # if called as a module (python -m fiar) run socket.io web server - eventlet
    socket_io = container.socket_io()
    socket_io.run(app)
