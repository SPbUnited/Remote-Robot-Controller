class Robot:
    MAX_DRIBBLER_SPEED = 15
    DR_SPEED_STEP_COUNT = 15

    MAX_CHARGE_VOLTAGE = 15
    VOLTAGE_STEP_COUNT = 15

    MAX_SPEED_VAL = 127

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

        self.robot_voltage = 0
        self.ball_checker = False
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

    def _validate_speed(self, speed):
        if speed is None:
            return 0
        if speed > self.MAX_SPEED_VAL:
            speed = self.MAX_SPEED_VAL
        if speed < -self.MAX_SPEED_VAL:
            speed = -self.MAX_SPEED_VAL
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

        buff = bytearray(6)

        packet_len = 12

        address_pos = 0
        speed_x_pos = 1
        speed_y_pos = 2
        speed_w_pos = 3
        dr_spd_n_ch_voltage_pos = 4
        # robot_voltage_pos = 5
        flags_pos = 5


        # ball_mask = 0x80
        force_kick_down_mask = 0x40
        force_kick_up_mask = 0x20
        kick_up_mask = 0x10
        kick_down_mask = 0x08
        beep_mask = 0x04
        dribbler_en_mask = 0x02
        charge_en_mask = 0x01

        # speed_dribbler_pos = 4
        # kicker_voltage_level_pos = 5
        # kick_up_pos = 6
        # kick_forward_pos = 7
        # beeper_state_pos = 8
        # dribbler_enable_pos = 9
        # kicker_charge_enable_pos = 10
        # force_kick_state_pos = 11

        # wp_op_code = bytes(0x10)
#        print(self.speed_x, self.speed_y)

        op_addr = int(self.address).to_bytes(1, 'big', signed=False)[0]

        buff[address_pos] = op_addr
        buff[speed_x_pos] = self.speed_x.to_bytes(1, 'big', signed=True)[0]
        buff[speed_y_pos] = self.speed_y.to_bytes(1, 'big', signed=True)[0]
        buff[speed_w_pos] = self.speed_w.to_bytes(1, 'big', signed=True)[0]
        # buff[robot_voltage_pos] = self.robot_voltage.to_bytes(1, 'big', signed=True)[0]

        buff[dr_spd_n_ch_voltage_pos] = self.dribbler_speed.to_bytes(1, 'big', signed=False)[0]

        buff[dr_spd_n_ch_voltage_pos] += self.kicker_voltage.to_bytes(1, 'big', signed=False)[0] << 4

        buff[flags_pos] = charge_en_mask * self.charge_en
        buff[flags_pos] += dribbler_en_mask * self.dribbler_en
        buff[flags_pos] += beep_mask * self._beep_flag
        buff[flags_pos] += force_kick_up_mask * self._kick_up_flag  # * (not self.auto_kick_upper)
        buff[flags_pos] += force_kick_down_mask * self._kick_down_flag  # * self.auto_kick_upper
        buff[flags_pos] += kick_up_mask * self.auto_kick_en * self.auto_kick_upper
        buff[flags_pos] += kick_down_mask * self.auto_kick_en * (not self.auto_kick_upper)
        # buff[flags_pos] += ball_mask * self.ball_checker

        return buff

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

                "robot_voltage": self.robot_voltage,
                "ball_checker": self.ball_checker

                # Instant actions flags
                # self._kick_up_flag ,
                # self._kick_down_flag,
                # self._beep_flag
            }
        return msg

    def set_from_api(self, data):

        self.set_speed(data["speed_x"], data["speed_y"], data["speed_w"])
        self.dribbler_speed = int(self.MAX_DRIBBLER_SPEED / self.DR_SPEED_STEP_COUNT * data["dribbler_speed"])
        self.kicker_voltage = int(self.MAX_CHARGE_VOLTAGE / self.VOLTAGE_STEP_COUNT * data["kicker_voltage"])
        self.kick_up(not data["kick_up"])
        self.kick_down(not data["kick_down"])
        self.beep(not data["beep"])
        self.dribbler_en = data["dribbler_en"]
        self.charge_en = data["charge_en"]

        if data["autokick"] == 0:
            self.auto_kick_en = False
            self.auto_kick_upper = False
        if data["autokick"] == 1:
            self.auto_kick_en = True
            self.auto_kick_upper = False
        if data["autokick"] == 2:
            self.auto_kick_en = True
            self.auto_kick_upper = True
        pass
    
    def set_from_serial(self, data):
        self.robot_voltage = data["robot_voltage"]
        self.ball_checker = data["ball_checker"]
        pass
