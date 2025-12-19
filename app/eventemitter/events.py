import asyncio
import json as jsons


def load_events(app, ee):
    rsv = None

    @ee.on('sys:start')
    async def sys_start_handler():
        try:
            print('system started')
            # await app.input_listner.run()
            await asyncio.sleep(0.5)

        except Exception as e:
            print(f"Exception 1 in {__file__}: {str(e)}")
            pass

    @ee.on('sys:start')
    async def sys_start_handler():
        try:
            await app.bot_controller.bot_sender()
            a =2
        except Exception as e:
            print(f"Exception 2 in {__file__}: {str(e)}")
            pass

    @ee.on('sys:start')
    async def sys_start_handler():
        try:
            await app.bot_controller.udp_listener()
            a =2
        except Exception as e:
            print(f"Exception 3 in {__file__}: {str(e)}")
            pass

    @ee.on('sys:start')
    async def sys_start_handler():
        try:
            await app.bot_controller.serial_listener()
            a =3 
            # await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Exception 4 in {__file__}: {str(e)}")
            pass

        
    
    @ee.on('sys:start')
    async def sys_start_handler():
        try:
            while True:
                # await app.input_listner.run()
                msg = app.bot_controller.get_state()
                # msg = json(msg)
                string = jsons.dumps(msg)
                await app.web.send_all_webclient(string)
                # await ws.send(string)
                await asyncio.sleep(0.1)

        except Exception as e:
            print(f"Exception 5 in {__file__}: {str(e)}")
            pass

    @ee.on('sys:stop')
    def sys_stop_handler():
        try:
            print('system stopping')
        except:
            pass

    @ee.on('workflow:new')
    async def wrkflow_send(message):
        try:
            print('system stopping')
        except:
            pass

    @ee.on('workflow:update')
    async def updateworkflow(message):
        try:
            print('workflow:update')
        except:
            pass
