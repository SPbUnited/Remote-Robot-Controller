import json
import asyncio
import traceback

from sanic import Sanic
import sanic.response as response
from sanic.exceptions import ServerError
from .routes import *
from websockets.exceptions import ConnectionClosed
from sanic_cors import CORS, cross_origin

class Web:
    def __init__(self, app) -> None:
        super().__init__()

        self.__app = app

        self.ee = app.event_emitter
        self.loop = app.loop
        self.sanic = Sanic(__name__)

        self.config = app.config['web']
        self.sanic.config.update(self.config['sanic'])


        self.ctrlclient = None
        self.web_clients = []
        # self.debugclients = []

        # CORS(self.sanic, resources={r"/api/*": {"origins": "*"}}, automatic_options=True)
        # self.vidctrl = app.vidctrl
        self.counter = 0
        self.reset_resp = False

        load_routes(self, app)
        load_ws(self, app)

    @property
    def app(self):
        return self.__app

    def route(self, url, methods=None, fn=None):

        if methods is None:
            methods = ['GET']

        def _route(fn):

            async def fn_executor(*args, **kwargs):
                error = None
                try:
                    result = fn(*args, **kwargs)

                    if asyncio.iscoroutine(result):
                        result = await result

                    return response.json(result)
                except ServerError as e:
                    print(f"Exception 1 in {__file__}: {str(e)}")
                    error = ServerError(
                        data=e.params,
                        message='Api command error',
                        error=e.__class__.__name__,
                        trace=traceback.format_exc().split('\n'),
                        code=400
                    )
                except (ServerError, ServerError, ServerError) as e:
                    print(f"Exception 2 in {__file__}: {str(e)}")
                    error = ServerError(
                        data=e.to_json(),
                        error=e.__class__.__name__,
                        message=e.message,
                        trace=traceback.format_exc().split('\n')
                    )
                except Exception as e:
                    print(f"Exception 3 in {__file__}: {str(e)}")
                    error = ServerError(
                        data={'message': e.args[0]} if hasattr(e, 'args') and len(e.args) > 0 else e.__dict__,
                        error=e.__class__.__name__,
                        message='Internal Server Error',
                        trace=traceback.format_exc().split('\n'),
                        code=500
                    )

                return response.json(error.to_json(), status=error.code)

            self.sanic.add_route(fn_executor, url, methods=methods)
            return fn

        if fn is None:
            return _route

        return _route(fn)

    def start(self):
        server = self.sanic.create_server(host=self.config['host'],
                                          port=self.config['port'],
                                          return_asyncio_server=True)
        task = asyncio.ensure_future(server)

    async def add_ctrlclient(self, socket):
        if self.ctrlclient:
            await self.remove_ctrlclient(self.ctrlclient)
            self.counter = 0
        self.ctrlclient = socket

    def add_web_client(self, socket):
        self.web_clients.append(socket)

    # def add_debugclient(self, socket):
    #     self.debugclients.append(socket)
    #
    async def remove_ctrlclient(self, socket):
        try:
            await self.ctrlclient.close()
            self.ctrlclient = None
        except ValueError:
            pass  # already removed

    def remove_web_client(self, socket):
        try:
            self.web_clients.remove(socket)
        except ValueError:
            pass  # already removed
    #
    # def remove_debugclient(self, socket):
    #     try:
    #         self.debugclients.remove(socket)
    #     except ValueError:
    #         pass  # already removed

    async def send_vidctrl_client(self, data, noresp=False):
        if self.ctrlclient:
            try:
                await self.ctrlclient.send(json.dumps(data))
                if noresp:
                    return
                return await self.await_resp()
            except ConnectionClosed:
                await self.remove_ctrlclient(self.ctrlclient)
                return False

    async def send_all_webclient(self, data):
        for socket in self.web_clients:
            try:
                await socket.send(data)
            except ConnectionClosed as e:
                self.remove_web_client(socket)
    #
    # async def send_all_debugclients(self, data):
    #     for socket in self.debugclients:
    #         try:
    #             await socket.send(data)
    #         except ConnectionClosed:
    #             self.remove_debugclient(socket)

    async def await_resp(self):
        self.reset_resp = False
        while not self.reset_resp:
            await asyncio.sleep(0.5)
            pass
        return True
