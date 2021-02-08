from fiar import app

if __name__ == '__main__':
    # if called as a module (python -m fiar) run socket.io web server - eventlet
    app.socket_io.run(app)
