def load_events(app, ee):
    rsv = None
    @ee.on('sys:start')
    async def sys_start_handler():
        try:
            print('system started')
            # await app.input_listner.run()
        except Exception as e:
            print(e)
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