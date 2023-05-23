import serial


class Serial_Listener:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
        self.ser.flush()
        pass

    async def listen(self):
        try:
            recv = self.ser.read_until('&')
        except serial.SerialTimeoutException:
            return None
        
        if recv[0] != 0x01:
            return None

        data = \
            {
                # "bot_number": int.from_bytes(raw[1], byteorder="big", signed=False),
                # "speed_x": int.from_bytes(raw[2], byteorder="big", signed=True),
                # "speed_y": int.from_bytes(raw[3], byteorder="big", signed=True),
                # "speed_w": int.from_bytes(raw[4], byteorder="big", signed=True),
                # "dribbler_speed": int.from_bytes(raw[5], byteorder="big", signed=False),
                # "kicker_voltage": int.from_bytes(raw[6], byteorder="big", signed=False),
                # "kick_up": bool(int.from_bytes(raw[7], byteorder="big", signed=False)),
                # "kick_down": bool(int.from_bytes(raw[8], byteorder="big", signed=False)),
                # "beep": bool(int.from_bytes(raw[9], byteorder="big", signed=False)),
                # "dribbler_en": bool(int.from_bytes(raw[10], byteorder="big", signed=False)),
                # "charge_en": bool(int.from_bytes(raw[11], byteorder="big", signed=False)),
                # "autokick": int.from_bytes(raw[12], byteorder="big", signed=False)
                "bot_number": recv[1],
                "robot_voltage": recv[2],
                "ball_cheker": recv[3]

            }

        return data
