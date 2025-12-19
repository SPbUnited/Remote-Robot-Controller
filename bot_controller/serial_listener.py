import struct
import time

import board
import busio
import digitalio as dio
from circuitpython_nrf24l01.rf24 import RF24


class Reciever:

    def __init__(self):

        # D10 MOSI
        # D9 MSIO
        # D8 C0EN
        ce = dio.DigitalInOut(board.D16)
        csn = dio.DigitalInOut(board.D26)

        # spi = board.SPI()  # init spi bus object
        spi = busio.SPI(board.SCLK_1, board.MOSI_1, board.MISO_1)
        # spi.try_lock()
        # spi.configure(baudrate=125)
        # spi.unlock()

        self.nrf = RF24(spi, csn, ce)  # , payload_length=6, auto_ack=False, dynamic_payloads=False)

        self.nrf.data_rate = 2
        self.nrf.crc = 2
        self.nrf.address_length = 3

        # addr
        # uint8_t ADDR0[] = {0xAB, 0xAD, 0xAF}
        self.address = bytearray([0xAB, 0xAD, 0xAF])
        # self.address = bytearray([0xAF, 0xAD, 0xAB])
        # self.nrf.dynamic_payloads = False
        # self.nrf.payload_length = 7

        self.nrf.pa_level = 0
        self.nrf.auto_ack = False

        self.nrf.channel = 76
        self.nrf.listen = True
        self.nrf.power = True

        self.nrf.open_rx_pipe(1, self.address)
        self.nrf.print_details(True)
        # uint8_t ADDR0[] = {0xAB, 0xAD, 0xAF}; // the address for RX pipe
        # m_nrf24.setRfChannel(76); // set RF channel to 2400 + channel[MHz]
        # m_nrf24.setDataRate(Nrf24DataRate::NRF24_DR_2Mbps); // 2 Mbit / s data rate
        # m_nrf24.setCrcScheme(Nrf24Crc::NRF24_CRC_2_BYTE); // 2 - byte  CRC scheme
        # m_nrf24.setAddrWidth(Nrf24SetupAddressWidth::NRF24_ADDRESS_WIDTH_3_BYTE); // address width is 5 bytes
        # // m_nrf24.setAddr(Nrf24RxpipeAddresses::NRF24_PIPETX, ADDR); // program TX address
        # m_nrf24.setAddr(Nrf24RxpipeAddresses::NRF24_PIPE0, ADDR0); // program pipe address
        # // m_nrf24.setAddr(Nrf24RxpipeAddresses::NRF24_PIPETX, ADDR0); // program pipe address
        # m_nrf24.setRxPipe(Nrf24RxpipeAddresses::NRF24_PIPE0, NRF24_AA_OFF, m_incomePacketLen); // enable RX pipe  # 1 with Auto-ACK: enabled, payload length: 10 bytes
        # // m_nrf24.setTxPower(Nrf24RfPower::NRF24_TXPWR_18dBm); // configure TX power for Auto - ACK, good choice - same power level as on transmitter
        # m_nrf24.setOperationMode(Nrf24OperationMode::NRF24_Operation_PRX); // switch transceiver to the RX mode
        # // m_nrf24.enableAa(Nrf24RxpipeAddresses::NRF24_PIPE0);
        # m_nrf24.setPowerMode(Nrf24Power::NRF24_PWR_UP); // wake - up transceiver( in case if it sleeping)

        pass
    
    def recv(self):
        print('Trying')
        if self.nrf.available():
            print('Availabe')
            payload_length = self.nrf.any()  # Returns 0 if no payload
 #           print(i)
#            i+=1
            if payload_length:
                # Read payload as bytes
                payload = bytes(self.nrf.read(payload_length))
                print(payload)
                # Try to decode as UTF-8 string command
                try:
                    cmd = payload.decode("ascii").strip()
                except UnicodeDecodeError:
                    # Fall back to hex representation for binary data
                    cmd = payload.hex()
                print(f"RX command: {cmd!r}, len {len(cmd)}")
                # print()
                return len(cmd)
        return 0


    def send(self, buff, addr=None):
        # self.nrf.open_tx_pipe(addr)

        if addr is not None:
            old_addr = self.address
            self.address = addr
            result = self.nrf.send(buff)
            self.address = old_addr
        else:
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
# tr.send(buff)

#
# while True:
#     tr.send(bytearray(b'1Node'), buff)
# # tr.master_test()
# buff = bytearray(6 * 4)
#
# op_addr = 0x10.to_bytes(1, 'big')[0] + int(255).to_bytes(1, 'big')[0]
#
# smth = 1
#
# buff[0] = op_addr
# buff[0] = op_addr
# buff[6] = smth
# buff[0] = op_addr
