import asyncio
import datetime
import subprocess


from .robot import Robot
from .transmitter import Transmitter
from .udp_listner import UDPListner
from .serial_listener import Reciever
# from .udp_transmitter import UDPTransmitter
# from .serial_listener import Serial_Listener

class BotController:
    ROBOT_COUNT = 8
    MAX_SPEED_VAL = Robot.MAX_SPEED_VAL
    SPEED_RANGE_COUNT = 3
    ROBOT_OFFSET = 240 # 248

    def __init__(self, app):
        self.robots = []
        self.selected_bot_index = 0
        self.selected_bot = None
        self.speed_range = 0

        self.bot_by_number = {}

        i = 0
        while i < self.ROBOT_COUNT:
            self.robots.append(Robot(i + self.ROBOT_OFFSET))
            self.bot_by_number[i + self.ROBOT_OFFSET] = self.robots[i]
            i += 1
        self.selected_bot = self.robots[self.selected_bot_index]

        self.tx = Transmitter()

        self.udp = UDPListner()

        self.udpT = UDPTransmitter()

        self.uart = Reciever()

        self.old_msg = {"speed_x": None, "speed_y": None, "speed_w": None,
                        "kick_up": None, "kick_down": None, "beep": None}

        ip4_output = subprocess.run(['nmcli', '--fields', 'IP4.ADDRESS', 'device', 'show', 'eth0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # self.box_ip = ip4_output.split()[1][:-3]

        pass

    def set_speed_n_triggers(self, msg):
        try:
            for key in self.old_msg.keys():
                if msg[key] != self.old_msg[key]:
                    self.set_speed(speed_x=msg["speed_x"], speed_y=msg["speed_y"], speed_w=msg["speed_w"])
                    self.selected_bot.kick_up(not msg["kick_up"])
                    self.selected_bot.kick_down(not msg["kick_down"])
                    self.selected_bot.beep(not msg["beep"])
                    break
            for key in self.old_msg.keys():
                self.old_msg[key] = msg[key]

        except Exception as e:
            print(f"Exception 1 in {__file__}: {str(e)}")
            pass
        pass

    def set_speed(self, speed_x=None, speed_y=None, speed_w=None, ignore_range=False):
        speed_multiplier = (self.speed_range + 1) / self.SPEED_RANGE_COUNT
        if ignore_range:
            speed_multiplier = 1
        if speed_x is not None:
            speed_x = speed_x * speed_multiplier
        if speed_y is not None:
            speed_y = speed_y * speed_multiplier
        if speed_w is not None:
            speed_w = -speed_w * speed_multiplier
        self.selected_bot.set_speed(speed_x, speed_y, speed_w)
        pass

    def switch_bot(self):
        self.selected_bot_index += 1
        if self.selected_bot_index >= self.ROBOT_COUNT:
            self.selected_bot_index = 0
        self.selected_bot.stop()
        self.selected_bot = self.robots[self.selected_bot_index]

    def switch_speed_range(self):
        self.speed_range += 1
        if self.speed_range >= self.SPEED_RANGE_COUNT:
            self.speed_range = 0
        pass

    def stop(self):
        self.selected_bot.stop()
        pass

    def stop_all(self):
        for robot in self.robots:
            robot.stop()
        pass

    def get_state(self):
        msg = \
            {
                "box_ip": self.box_ip,
                "selected_bot": self.selected_bot_index,
                "speed_range": self.speed_range
            }
        for robot in self.robots:
            msg["robot_" + str(robot.address - self.ROBOT_OFFSET)] = robot.get_state()

        return msg

    async def bot_sender(self):
        ts = datetime.datetime.now()
        while True:
#            await asyncio.sleep(.002)
            try:
                # print('au')
                for bot in self.robots:
                    # print("Before:")
                    # print((datetime.datetime.now() - ts).microseconds)
                    # ts = datetime.datetime.now()
                    # self.tx.send(self.selected_bot.serialize_to_bot())
                    # print('ale')
                    self.tx.send(bot.serialize_to_bot())
                    
                    # print("After:")
                    # print((datetime.datetime.now() - ts).microseconds)
                    # ts = datetime.datetime.now()
                    await asyncio.sleep(.002)
            except Exception as e:
                print(f"Exception 2 in {__file__}: {str(e)}")
                continue
        pass

    async def udp_listener(self):
        ts = datetime.datetime.now()
        while True:
#            await asyncio.sleep(.0002)
            try:
                data = await self.udp.listen()
                if data is not None:
#                    continue
                    if "debug_override" in data:
                        self.tx.send(data["payload"])
                    else:
                        number = data["bot_number"]  # + self.ROBOT_OFFSET
                        if number in self.bot_by_number:
                            self.bot_by_number[number].set_from_api(data)
                await asyncio.sleep(.0002)
            except Exception as e:
                print(f"Exception 3 in {__file__}: {str(e)}")
                continue
        pass

    async def serial_listener(self):
        ts = datetime.datetime.now()
        while True:
            try:
                # print('here')
                recv_value = self.uart.recv()
                if recv_value is not None:
                    self.udpT.send(recv_value[1:])
                    print(recv_value[1:])
                await asyncio.sleep(.002)
            except Exception as e:
                print(f"Exception 4 in {__file__}: {str(e)}")
                continue
        pass
