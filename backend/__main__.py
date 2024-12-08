import webbrowser
from backend.app import create_app

if __name__ == '__main__':
    app, socketio, snake = create_app()
    webbrowser.open('http://localhost:5000/')
    snake.start()
    socketio.run(
        app=app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=True
    )
