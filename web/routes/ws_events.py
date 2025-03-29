# from sanic.response import json
import json as jsons
from datetime import datetime

def load_ws(web, app):

    @web.ee.on('client:connect')
    async def client_connect():
        print('client connected')
        # await web.send_vidctrl_client(jsons.dumps({
        #     'event': 'client:connect',
        #     'timestamp': datetime.now().isoformat()
        # }))

    @web.ee.on('printer:connect')
    async def client_connect():
        print('printer connected')
        await web.send_vidctrl_client(jsons.dumps({
            'event': 'printer:connect',
            'timestamp': datetime.now().isoformat()
        }))

    @web.ee.on('debug:connect')
    async def client_connect():
        print('debug connected')
        # await web.send_reset(jsons.dumps({
        #     'event': 'debug:connect',
        #     'timestamp': datetime.now().isoformat()
        # }))

    @web.ee.on('rst:update')
    async def rst_update():
        await web.send_all_webclient("update")
