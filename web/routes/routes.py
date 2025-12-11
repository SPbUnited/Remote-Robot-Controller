import asyncio
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
    async def bot_beep(req):
        app.bot_controller.selected_bot.beep()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/switch_bot', methods=['PUT'])
    async def switch_bot(req):
        app.bot_controller.switch_bot()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/switch_speed_range', methods=['PUT'])
    async def switch_speed_range(req):
        app.bot_controller.switch_speed_range()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/toggle_dribbler', methods=['PUT'])
    async def toggle_dribbler(req):
        app.bot_controller.selected_bot.toggle_dribbler()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/toggle_charge', methods=['PUT'])
    async def toggle_charge(req):
        app.bot_controller.selected_bot.toggle_charge()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/switch_autokick', methods=['PUT'])
    async def switch_autokick(req):
        app.bot_controller.selected_bot.switch_autokick()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/voltage_up', methods=['PUT'])
    async def voltage_up(req):
        app.bot_controller.selected_bot.voltage_up()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/voltage_down', methods=['PUT'])
    async def voltage_down(req):
        app.bot_controller.selected_bot.voltage_down()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/dribbler_speed_up', methods=['PUT'])
    async def dribbler_speed_up(req):
        app.bot_controller.selected_bot.dribbler_speed_up()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/dribbler_speed_down', methods=['PUT'])
    async def dribbler_speed_down(req):
        app.bot_controller.selected_bot.dribbler_speed_down()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/kick_up', methods=['PUT'])
    async def kick_up(req):
        app.bot_controller.selected_bot.kick_up()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/kick_down', methods=['PUT'])
    async def kick_down(req):
        app.bot_controller.selected_bot.kick_down()
        return json({"resp": "ok"})

    @sanic.route('/api/bot/stop_all', methods=['PUT'])
    async def kick_down(req):
    #    app.bot_controller.stop_all()
        return json({"resp": "ok"})

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
                # print('Got:' + message)
                message = jsons.loads(message)
                if message["command"] == "speed_n_triggers":
                    web.app.bot_controller.set_speed_n_triggers(message)

            except ConnectionClosed:
                web.app.bot_controller.stop()
                web.remove_webclient(ws)
                break

    # @sanic.websocket('/api/ctrlclient')
    # async def api_ctrlclient(request, ws):
    #     app.event_emitter.emit('client:connect')
    #     web.add_ctrlclient(ws)
    #     while True:
    #         try:
    #
    #         except ConnectionClosed:
    #             web.remove_ctrlclient(ws)
    #             break
