from inputs import get_gamepad
from inputs import DeviceManager
import inputs
from .ctrl_input import BotController


class InputListner:

    def __init__(self):
        self._events = None

        self._bot_controller = BotController()
        self._devices = inputs.devices

        self._current_robot = 0
        self._robot_count = 8

        pass

    async def run(self):
        while True:
            self._events = await get_gamepad()
            for event in self._events:
                if event.code == 'ABS_HAT0Y':
                    if event.state == 0:
                        self._bot_controller.stop_fb()
                    if event.state == -1:
                        self._bot_controller.move_forward()
                    if event.state == 1:
                        self._bot_controller.move_backward()
                    self._bot_controller.print_speed()
                    continue

                if event.code == 'ABS_HAT0X':
                    if event.state == 0:
                        self._bot_controller.stop_lr()
                    if event.state == -1:
                        self._bot_controller.move_left()
                    if event.state == 1:
                        self._bot_controller.move_right()
                    self._bot_controller.print_speed()
                    continue

                if event.code == 'ABS_Z':
                    self._bot_controller.set_rot(-event.state)
                    self._bot_controller.print_speed()
                    continue

                if event.code == 'ABS_RZ':
                    self._bot_controller.set_rot(event.state)
                    self._bot_controller.print_speed()
                    continue

                if event.code == 'BTN_SELECT':
                    if event.state == 0:
                        self._current_robot += 1
                        if self._current_robot >= self._robot_count:
                            self._current_robot = 0
                        print("Bot selected: " + str(self._current_robot))
                    continue

                pass
                # print(event.ev_type, event.code, event.state)

        pass

    async def as_ru(self):
        self._events = await get_gamepad()
        pass
