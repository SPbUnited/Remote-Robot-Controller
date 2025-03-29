# import socket


# class UDPTransmitter:

#     def __init__(self):
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         UDP_IP = "0.0.0.0"
#         UDP_PORT = 10000
#         self.sock.bind((UDP_IP, UDP_PORT))
#         self.sock.settimeout(.002)
#         pass

#     def send(self, buff, addr=None):
#         result = self.sock.sendall(buff)
#         return result

        
