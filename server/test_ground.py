from threading import Thread
import socket
from time import sleep

cmd_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#
spectrum_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10101
sound_in= socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10103


spectrum_in.connect( ('127.0.0.1', 10102))
sound_in.connect(('127.0.0.1', 10104))


for i in range(10):
    cmd_out.sendto(b'1',('127.0.0.1',10105))
    data=spectrum_in.recv(4)
    print(data)
