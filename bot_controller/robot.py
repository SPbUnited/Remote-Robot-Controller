class Robot:
    MAX_DRIBBLER_SPEED = 255
    DR_SPEED_STEP_COUNT = 15

    MAX_CHARGE_VOLTAGE = 255
    VOLTAGE_STEP_COUNT = 15

    def __init__(self, address):
        self.address = address

        self.speed_x = 0
        self.speed_y = 0
        self.speed_w = 0

        self.dribbler_speed = 0
        self.dribbler_en = False

        self.kicker_voltage = 0
        self.charge_en = False

        self.auto_kick_en = False
        self.auto_kick_upper = False

        # Instant actions flags
        self._kick_up_flag = False
        self._kick_down_flag = False
        self._beep_flag = False

        pass

    def switch_autokick(self):
        if not self.auto_kick_en:
            self.auto_kick_en = True
            self.auto_kick_upper = False
        else:
            if not self.auto_kick_upper:
                self.auto_kick_en = True
                self.auto_kick_upper = True
            else:
                self.auto_kick_en = False
                self.auto_kick_upper = False

        pass



    @staticmethod
    def _validate_speed(speed):
        if speed is None:
            return 0
        if speed > 255:
            speed = 255
        if speed < -255:
            speed = -255
        return int(speed)

    def set_speed(self, speed_x=None, speed_y=None, speed_w=None):
        if speed_x is not None:
            self.speed_x = self._validate_speed(speed_x)
        if speed_y is not None:
            self.speed_y = self._validate_speed(speed_y)
        if speed_w is not None:
            self.speed_w = self._validate_speed(speed_w)
        pass

    def beep(self, reset=False):
        self._beep_flag = not reset
        pass

    def kick_up(self, reset=False):
        self._kick_up_flag = not reset
        pass

    def kick_down(self, reset=False):
        self._kick_down_flag = not reset
        pass

    def toggle_charge(self):
        self.charge_en = not self.charge_en
        pass

    def toggle_dribbler(self):
        self.dribbler_en = not self.dribbler_en
        pass

    def voltage_up(self):
        target_voltage = self.kicker_voltage + self.MAX_CHARGE_VOLTAGE / self.VOLTAGE_STEP_COUNT
        if target_voltage >= self.MAX_CHARGE_VOLTAGE:
            target_voltage = self.MAX_CHARGE_VOLTAGE
        self.kicker_voltage = int(target_voltage)
        pass

    def voltage_down(self):
        target_voltage = self.kicker_voltage - self.MAX_CHARGE_VOLTAGE / self.VOLTAGE_STEP_COUNT
        if target_voltage <= 0:
            target_voltage = 0
        self.kicker_voltage = int(target_voltage)
        pass

    def dribbler_speed_up(self):
        target_speed = self.dribbler_speed + self.MAX_DRIBBLER_SPEED / self.DR_SPEED_STEP_COUNT
        if target_speed >= self.MAX_DRIBBLER_SPEED:
            target_speed = self.MAX_DRIBBLER_SPEED
        self.dribbler_speed = int(target_speed)
        pass

    def dribbler_speed_down(self):
        target_speed = self.dribbler_speed - self.MAX_DRIBBLER_SPEED / self.DR_SPEED_STEP_COUNT
        if target_speed <= 0:
            target_speed = 0
        self.dribbler_speed = int(target_speed)
        pass

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_w = 0

        self.dribbler_en = False

        self.charge_en = False

        # Instant actions flags
        self._kick_up_flag = False
        self._kick_down_flag = False
        self._beep_flag = False
        pass

    #  Serializes bot state
    def serialize_to_bot(self):
        return None

    def get_state(self):
        msg = \
            {
                "address": self.address,

                "speed_x": self.speed_x,
                "speed_y": self.speed_y,
                "speed_w": self.speed_w,

                "dribbler_speed": self.dribbler_speed,
                "dribbler_en": self.dribbler_en,

                "kicker_voltage": self.kicker_voltage,
                "charge_en": self.charge_en,

                "auto_kick_en": self.auto_kick_en,
                "auto_kick_upper": self.auto_kick_upper,

                # Instant actions flags
                # self._kick_up_flag ,
                # self._kick_down_flag,
                # self._beep_flag
            }
        return msg
