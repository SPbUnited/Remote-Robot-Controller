import socket


class UDPListner:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_IP = "0.0.0.0"
        UDP_PORT = 10000
        self.sock.bind((UDP_IP, UDP_PORT))
        self.sock.setblocking(False)
#        self.sock.settimeout(.002)
        pass

    async def listen(self):
        try:
            raw, addr = self.sock.recvfrom(13)
        except:# socket.timeout:
#            pass
            return None
        if raw[0] == 0x01:
            print(raw)
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
                    "bot_number": raw[1],
                    "speed_x": raw[2] if raw[2] <= 127 else raw[2]-256,
                    "speed_y": raw[3] if raw[3] <= 127 else raw[3]-256,
                    "speed_w": raw[4] if raw[4] <= 127 else raw[4]-256,
                    "dribbler_speed": raw[5],
                    "kicker_voltage": raw[6],
                    "kick_up": bool(raw[7]),
                    "kick_down": bool(raw[8]),
                    "beep": bool(raw[9]),
                    "dribbler_en": bool(raw[10]),
                    "charge_en": bool(raw[11]),
                    "autokick": raw[12]

                }

            return data
        elif raw[0] == 0xDE:
            data = \
            {
                "debug_override": True,
                "payload": raw[1:]
            }
        
        return None
