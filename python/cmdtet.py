import socket
import time
cmd_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST='119.29.209.127'
def fmdm():
    cmd_in.sendto(b'\x00\x01\x03\x00',(HOST,10104))
def fft():
    cmd_in.sendto(b'\x00\x01\x04\x00',(HOST,10104))
def stop():
    cmd_in.sendto(b'\x00\x01\x05\x00',(HOST,10104))
def quit():
    cmd_in.sendto(b'\x00\x01\x05\x00',(HOST,10104))
    time.sleep(5)
    cmd_in.sendto(b'\x00\x01\x06\x00',(HOST,10104))
