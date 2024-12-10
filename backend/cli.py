from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import webbrowser
from backend import __version__
from backend.app import create_app
from backend.config import Config


def parse_arguments(args: list[str]):

    p = ArgumentParser(
        description="Snake AI",
        conflict_handler='resolve',
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    p.add_argument(
        '-v', '-V', '--version',
        action='version',
        help='show the version number',
        version=f'version is {__version__}'
    )

    p.add_argument('--start-game', action='store_true', help='starts the game')
    p.add_argument('--height', type=int, default=16,
                   help='height of the board')
    p.add_argument('--width', type=int, default=32, help='width of the board')
    p.add_argument('--open-browser', action='store_true',
                   help='open browser at startup')
    p.add_argument('--host', type=str, default='localhost',
                   help='host of the web server')
    p.add_argument('--port', type=int, default=5000,
                   help='port of the web server')
    p.add_argument('--debug', action='store_true', help='debug mode')

    return p.parse_args(args)


def cli(argv: list[str] | None = None):

    try:
        args = parse_arguments(argv)

    except Exception as e:
        print('Sorry, something went wrong when parsing the given arguments')
        print(e)
        print(type(e))

    try:

        if args.start_game:
            print('Starting game...')
            app, socketio, snake = create_app(
                height=args.height,
                width=args.width,
                config_class=Config())

            if args.open_browser:
                webbrowser.open(f'http://{args.host}:{args.port}/')

            snake.start()

            socketio.run(
                app=app,
                host=args.host,
                port=args.port,
                debug=args.debug
            )

    except Exception as e:
        print('Sorry, something went wrong when starting the game')
        print(e)
        print(type(e))
