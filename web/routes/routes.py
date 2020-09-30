import os
import json as jsons
from sanic.response import file, json
from sanic.exceptions import NotFound, ServerError
from websockets.exceptions import ConnectionClosed
from os import path


# from db.db import DB

def load_routes(web, app):
    # ee = app.event_emitter
    root = app.root
    public = os.path.join(root, 'public')
    config = app.config['web']
    if config['public'] is not None:
        public = os.path.abspath(config['public'])

    assets = os.path.join(public, 'assets')

    # db = DB(app)

    sanic = web.sanic

    # static path
    sanic.static('/assets', assets)

    # WEB API
    @sanic.route('/')
    async def index(request):
        tmpl_file_path = path.join(public, 'index.html')
        return await file(tmpl_file_path)

    # RST

    @sanic.route('/api/rst', methods=['GET'])
    async def get_status(req):
        resp = app.vidctrl.rst_controller.get_status()
        return json(resp)  # jsons.loads(req.json)

    @sanic.route('/api/bot/beep', methods=['PUT'])
    async def start_feed(req):
        # resp = await app.vidctrl.rst_controller.start_feed()
        print("Beep!")
        return json({"resp": "ok"})

    # @sanic.route('/api/rst/stop_feed', methods=['PUT'])
    # async def stop_feed(req):
    #     resp = await app.vidctrl.rst_controller.stop_feed()
    #     return json(resp)
    #
    # @sanic.route('/api/rst/set_rx', methods=['PUT'])
    # async def set_rx(req):
    #     resp = await app.vidctrl.rst_controller.set_rx()
    #     return json(resp)
    #
    # @sanic.route('/api/rst/set_tx', methods=['PUT'])
    # async def set_tx(req):
    #     resp = await app.vidctrl.rst_controller.set_tx()
    #     return json(resp)

    #  Misc
    @sanic.exception(NotFound, ServerError)
    def json_404s(request, exception):
        return json({'error': exception})

    # @sanic.websocket('/api/vidctrl_client')
    # async def api_video_controller(request, ws):
    #     app.event_emitter.emit('debug:connect')
    #     await web.add_vidctrl_client(ws)
    #
    #     while True:
    #         try:
    #             message = await ws.recv()
    #             print('Got:' + message + "\t" + str(web.counter))
    #             message = jsons.loads(message)
    #             if message["command"] == "Ok":
    #                 web.reset_resp = True
    #                 continue
    #             response = {"target": message["target"], "command": "Ok"}
    #             app.vidctrl.incoming_message(message)
    #             await web.send_vidctrl_client(response, noresp=True)
    #             web.counter += 1
    #         except ConnectionClosed:
    #             await web.remove_vidctrl_client(ws)
    #             break
    #
    @sanic.websocket('/api/webclient')
    async def api_webclient(request, ws):
        app.event_emitter.emit('client:connect')
        web.add_web_client(ws)
        while True:
            try:
                message = await ws.recv()
                print('Got:' + message)
            except ConnectionClosed:
                web.remove_webclient(ws)
                break

