from threading import Thread
import socket
from time import sleep

spectrum_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10101
sound_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10103
cmd_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10106

spectrum_out.connect( ('127.0.0.1', 10101))
sound_out.connect(('127.0.0.1', 10103))
cmd_in.connect(('127.0.0.1', 10106))

data=cmd_in.recv(4)
spectrum_out.send(data)
