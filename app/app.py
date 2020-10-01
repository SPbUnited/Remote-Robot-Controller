import asyncio
import uvloop
import copy
import sys
import os
from signal import signal, SIGINT
from .eventemitter.eventemitter import event_emitter
from config import config
from web import Web
# from db.db import DB
from .daemon import Daemon
from bot_controller import BotController
# from video_controller import VideoController


class App(Daemon):
    def __init__(self, params) -> None:
        super().__init__(params['pidfile'])

        # app root path
        self.root = self.__detect_app_root()

        # config roots
        self.config_root = self.__detect_config_root()

        # getting a config
        self.config = config(self)

        # public root
        self.public_root = self.__detect_public_root()

        self.pid = params['pidfile']
        self.params = params

        # into initialize methon
        self.loop = None
        self.web = None
        self.input_listner = None
        self.bot_controller = None
        # self.vidctrl = None

        self.event_emitter = None
        # self.__system_config = None

        # self.db = None

    def __detect_app_root(self):

        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        elif __file__:
            return os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    '..'
                )
            )

    def __detect_config_root(self):
        _config_roots = []

        # if params['config_path']:
        #     _config_roots.append(params['config_path'])

        _config_roots.append(os.path.join(self.root, 'config'))
        _config_roots.append('/etc/autotrate')

        for path in _config_roots:
            if os.path.exists(path):
                return path

        return None

    def __detect_public_root(self):
        _config_roots = []

        if self.config['web']['public']:
            _config_roots.append(self.config['web']['public'])

        _config_roots.append(os.path.join(self.root, 'public'))
        _config_roots.append('/usr/local/autotrate/public')

        for path in _config_roots:
            if os.path.exists(path):
                return path

        return None

    # @property
    # def sysconfig(self):
    #     return self.__system_config

    def initialize(self):
        # init event loop
        asyncio.set_event_loop(uvloop.new_event_loop())
        # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.get_event_loop()

        # event emitter
        self.event_emitter = event_emitter(self)
        self.bot_controller = BotController(self)

        self.web = Web(self)
        # try:
        #     # self.input_listner = InputListner()
        # except Exception as e:
        #     print(e)
        #     self.input_listner = None

        self.event_emitter.emit('sys:init')

    def run_console(self):

        self.initialize()

        self.web.start()
        self.event_emitter.emit('sys:start')
        signal(SIGINT, lambda s, f: self.loop.stop())

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print('Keyboard stop')
            self.event_emitter.emit('sys:exit')
            self.event_emitter.emit('sys:stop')
            self.loop.stop()
        except Exception as e:
            print(str(e))
            self.event_emitter.emit('sys:error')
            self.event_emitter.emit('sys:stop')
            self.loop.stop()

    def stop_console(self):
        self.event_emitter.emit('sys:exit')
        self.event_emitter.emit('sys:stop')
        self.loop.stop()


    def run(self):

        self.initialize()

        self.web.start()
        self.event_emitter.emit('sys:start')
        signal(SIGINT, lambda s, f: self.loop.stop())

        # TODO: emit stop event while SIG will privided
        try:
            self.loop.run_forever()
        except Exception as e:
            print(str(e))
            self.event_emitter.emit('sys:error')
            self.stop()

    def reset(self):
        self.event_emitter.emit('sys:reset')

    def stop(self):
        # self.event_emitter.emit('sys:stop')
        # self.loop.stop()
        super().stop()
