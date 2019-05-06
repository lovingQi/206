from threading import Thread
import socket
from time import sleep
spectrum_in_addr      = ('', 10101)
spectrum_out_addr    = ('', 10102)
sound_in_addr            = ('', 10103)
sound_out_addr         = ('', 10104)
cmd_in_addr               = ('', 10105)
cmd_out_addr            = ('', 10106)

spectrum_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10101
spectrum_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10102
spectrum_in.bind(spectrum_in_addr)
spectrum_in.listen(1)
spectrum_out.bind(spectrum_out_addr)
spectrum_out.listen(30)

sound_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10103
sound_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#10104
sound_in.bind(sound_in_addr)
sound_in.listen(1)
sound_out.bind(sound_out_addr)
sound_out.listen(30)

cmd_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#
cmd_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#
cmd_in.bind(cmd_in_addr)
cmd_out.bind(cmd_out_addr)
cmd_out.listen(1)

server_DBG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

spectrum_in_cli=spectrum_in.accept()
sound_in_cli=sound_in.accept()
cmd_out_cli=cmd_out.accept()

spectrum_out_cli=spectrum_out.accept()
sound_out_cli=sound_out.accept()


def get_cli():
    global sound_out_cli
    global spectrum_out_cli
    while 1:
        spectrum_out_cli=spectrum_out.accept()
        sound_out_cli=sound_out.accept()
def sound_tran():
    global sound_out_cli
    while 1:
        data=sound_in_cli[0].recv(4)
        try:
            sound_out_cli[0].send(data)
        except:
            print('error')
def spectrum_tran():
    global spectrum_out_cli
    while 1:
        data=spectrum_in_cli[0].recv(4)
        print(data)
        try:
            spectrum_out_cli[0].send(data)
        except:
            print('error')
print('ok')
sound_tran_id=Thread(target=sound_tran)
sound_tran_id.start()
spectrum_tran_id=Thread(target=spectrum_tran)
spectrum_tran_id.start()
get_cli_id=Thread(target=get_cli)
get_cli_id.start()
while 1:
    cmd,addr=cmd_in.recvfrom(4)
    cmd_out_cli[0].send(cmd)






