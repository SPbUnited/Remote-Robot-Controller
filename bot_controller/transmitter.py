import struct
import time

import board
import digitalio as dio
from circuitpython_nrf24l01 import RF24


class Transmitter:

    def __init__(self):

        self.address = bytearray(b'1Node')

        # D10 MOSI
        # D9 MSIO
        # D8 C0EN
        ce = dio.DigitalInOut(board.D25)
        csn = dio.DigitalInOut(board.D8)

        spi = board.SPI()  # init spi bus object

        self.nrf = RF24(spi, csn, ce)

        pass

    def send(self, addr, buff):
        self.nrf.open_tx_pipe(addr)
        # ensures the nRF24L01 is in TX mode
        self.nrf.listen = False

        # out_buff = struct.pack(buff)

        result = self.nrf.send(buff)

        return result

    def master_test(self, count=5):  # count = 5 will only transmit 5 packets
        """Transmits an incrementing integer every second"""
        # set address of RX node into a TX pipe
        self.nrf.open_tx_pipe(self.address)
        # ensures the nRF24L01 is in TX mode
        self.nrf.listen = False

        while count:
            # use struct.pack to packetize your data
            # into a usable payload
            buffer = struct.pack('<i', count)
            # 'i' means a single 4 byte int value.
            # '<' means little endian byte order. this may be optional
            print("Sending: {} as struct: {}".format(count, buffer))
            now = time.monotonic() * 1000  # start timer
            result = self.nrf.send(buffer)
            if not result:
                print('send() failed or timed out')
            else:
                print('send() successful')
            # print timer results despite transmission success
            print('Transmission took',
                  time.monotonic() * 1000 - now, 'ms')
            time.sleep(1)
            count -= 1


# tr = Transmitter()
#
# buff = bytearray(b'123456789')
#
# while True:
#     tr.send(bytearray(b'1Node'), buff)
# # tr.master_test()
