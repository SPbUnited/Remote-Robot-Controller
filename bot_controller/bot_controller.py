import asyncio
import datetime

from .robot import Robot
from .transmitter import Transmitter
from .udp_listner import UDPListner


class BotController:
    ROBOT_COUNT = 8
    MAX_SPEED_VAL = Robot.MAX_SPEED_VAL
    SPEED_RANGE_COUNT = 3
    ROBOT_OFFSET = 1

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

        self.old_msg = {"speed_x": None, "speed_y": None, "speed_w": None,
                        "kick_up": None, "kick_down": None, "beep": None}

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
            print(e)
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
                "selected_bot": self.selected_bot_index,
                "speed_range": self.speed_range
            }
        for robot in self.robots:
            msg["robot_" + str(robot.address - self.ROBOT_OFFSET)] = robot.get_state()

        return msg

    async def bot_sender(self):
        ts = datetime.datetime.now()
        while True:
            try:
                for bot in self.robots:
                    # print("Before:")
                    # print((datetime.datetime.now() - ts).microseconds)
                    # ts = datetime.datetime.now()
                    # self.tx.send(self.selected_bot.serialize_to_bot())
                    self.tx.send(bot.serialize_to_bot())
                    # print("After:")
                    # print((datetime.datetime.now() - ts).microseconds)
                    # ts = datetime.datetime.now()
                    await asyncio.sleep(.002)
            except Exception as e:
                print(e)
                continue
        pass

    async def udp_listener(self):
        ts = datetime.datetime.now()
        while True:
            try:
                data = await self.udp.listen()
                if data:
                    number = data["bot_number"]  # + self.ROBOT_OFFSET
                    if number in self.bot_by_number:
                        self.bot_by_number[number].set_from_api(data)
                await asyncio.sleep(.002)
            except Exception as e:
                print(e)
                continue
        pass
