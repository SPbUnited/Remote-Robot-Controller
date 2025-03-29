

class BotController:
    def __init__(self):
        self._speed_x = 0
        self._speed_y = 0
        self._speed_w = 0

        self._def_speed = 255
        self._speed_multiplier = 1

    def _validate_speed(self, speed):
        if speed is None:
            return self._def_speed
        speed = int(speed)
        if speed > 255:
            speed = 255
        if speed < 255:
            speed = -255
        return speed

    def stop(self):
        self._speed_x = 0
        self._speed_y = 0
        self._speed_w = 0
        pass

    def move_forward(self, speed=None):
        self._speed_y += self._validate_speed(speed)
        pass

    def move_backward(self, speed=None):
        self._speed_y -= self._validate_speed(speed)
        pass

    def set_fb(self, speed=0):
        self._speed_y = self._validate_speed(speed)
        pass

    def stop_fb(self):
        self._speed_y = 0
        pass

    def move_right(self, speed=None):
        self._speed_x += self._validate_speed(speed)
        pass

    def move_left(self, speed=None):
        self._speed_x -= self._validate_speed(speed)
        pass

    def set_lr(self, speed=0):
        self._speed_x = self._validate_speed(speed)
        pass

    def stop_lr(self):
        self._speed_x = 0
        pass

    def rot_ccv(self, speed=None):
        self._speed_w += self._validate_speed(speed)
        pass

    def rot_cv(self, speed=None):
        self._speed_w -= self._validate_speed(speed)
        pass

    def set_rot(self, speed=0):
        self._speed_w = self._validate_speed(speed)
        pass

    def stop_rot(self):
        self._speed_w = 0
        pass

    def print_speed(self):
        print("Speed Y: " + str(self._speed_y))
        print("Speed X: " + str(self._speed_x))
        print("Speed W: " + str(self._speed_w))
        pass




# app = App()
# app.as_ru()
# app.run()
