import json
import requests
import argparse
from sys import exit
from app import App

__version__ = '0.3'

pid_file = '/var/run/print.pid'

def get_pid():
    try:
        with open(pid_file, 'r') as pf:

            pid = int(pf.read().strip())
    except IOError:
        pid = None

    return pid

def main():
    parser = argparse.ArgumentParser(
        description="cli command launcher"
    )

    parser.add_argument(
        'command',
        nargs='+',
        default='console',
        help='main command: start, stop, console - for starting/stopping daemon or running in console mode'
    )


    args = parser.parse_args()
    params = vars(args)
    params['pidfile'] = pid_file

    app = App(params)

    if args.command[0] == 'console':
        app.run_console()
    if args.command[0] == 'start':
        print('Version %s \n' % __version__, "Let's go!")
        app.start()
    elif args.command[0] == 'stop':
        app.stop()
    elif KeyboardInterrupt:
        app.stop_console()
    else:
        print('Wrong command argument: choose from ("start", "stop", "console" or "command [CMD] [DATA"])')