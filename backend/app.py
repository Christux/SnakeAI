import os, sys
import re
import uuid
from flask import Flask, Response, render_template
from flask_socketio import SocketIO
from backend.config import Config
from backend.snake.game import Snake

def read_file(path:str) -> str:
    with open(file=f'frontend/{path}', mode='r', encoding='utf-8') as f:
        return f.read()

def concatenate_files(path: str) -> str:
    content = ''
    entries = sorted(os.listdir(f'frontend/{path}'))
    for entry in entries:
        content += read_file(f'{path}/{entry}')
    return content

def minify_js(script: str) -> str:
    #script = re.sub(r'\r|\n', ' ', script)
    #script = re.sub(r'\s{2,}|\t', ' ', script)
    return script.strip()

def set_routes(app: Flask) -> None:

    @app.route('/')
    def index_page() -> str:
        return render_template('index.html', script_id=str(uuid.uuid4()), style_id=str(uuid.uuid4()))

    @app.route('/js/app.js-<id>')
    def bundle_scripts(id: str) -> Response:
        return Response(minify_js(concatenate_files('js')), mimetype='application/javascript')

    @app.route('/css/app.css-<id>')
    def bundel_stylesheets(id: str) -> Response:
        return Response(concatenate_files('css'), mimetype='text/css')

def set_socket(app: Flask, socketio: SocketIO, snake: Snake) -> None:

    def on_board_update(snake_indexes: str) -> None:
        with app.app_context():
            socketio.emit('update', snake_indexes)

    snake.on_update(on_board_update)

    @socketio.on('connect')
    def test_connect(auth):
        app.logger.info(auth)
        if snake.started:
            snake.stop_game()
        socketio.emit('init_board', snake.get_board_shape())

    @socketio.on('start')
    def start_game():
        snake.start_game()

    @socketio.on('pause')
    def pause_game():
        if snake.started:
            if snake.paused is False:
                snake.pause_game()
            else:
                snake.resume_game()
        else:
            snake.start_game()

    @socketio.on('stop')
    def stop_game():
        snake.stop_game()

    @socketio.on('direction')
    def onKeyPressed(data):
        snake.update_direction(data)

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    @socketio.on_error()        # Gère l'espace de noms par défaut
    def error_handler(e):
        app.logger.error('Une erreur s\'est produite : ' + str(e))
        socketio.emit('error_message', 'Une erreur s\'est produite : ' + str(e))


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../frontend/template')
    app.config.from_object(config_class)
    
    snake = Snake(16, 32)

    set_routes(app=app)
    socketio = SocketIO(app)
    set_socket(app=app, socketio=socketio, snake=snake)

    return app, socketio, snake
