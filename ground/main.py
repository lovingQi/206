import wave
import pyaudio 
import os
import numpy as np
from aip import AipSpeech
import socket
from threading import Thread
import time
import matplotlib.pyplot as plt
import scipy.signal as signal
import socket
#初始化
APP_ID = '10836826'
API_KEY = 'YvPbyRbqvwt0VDq8RK0GXRxF'
SECRET_KEY = 'GPIvnPuYf33OwSvYYf4bta2YN0HL0SBH'
DST=('192.168.3.120',10102)
CMDDST=('192.168.3.120',10102)
cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #建立一个基于UDP的Socket
loc=[]  #频点位置
scan=0#扫描开关
freq_list=np.array([88.5,93.7,101.1])
#语音识别
def reco(fname,client):
    with open(fname, 'rb') as fp:
        result=client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1537,})
        if result['err_no']==0:
            print(result['result'][0],end='')
        else:
            print(result['err_msg'])
            

thd={} # thread dictionary
max_seg=2#扫描段数
def fmdm():
    global thd
    global freq_list
    global max_seg
    count=0
    state=0
    now=0
    tt=0
    #sound output init
    p = pyaudio.PyAudio()
    #open sound output stream
    stream = p.open(format = p.get_format_from_width(2),channels = 1,rate = 48000, output = True)
    # socket init
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP Socket
    st.connect(('192.168.3.120',10101))
    print('fmdm  connect successful')
    
    #temp file init
    rec=wave.open('fm0.wav','wb')
    rec.setnchannels(1)
    rec.setsampwidth(2)
    rec.setframerate(16000)

    
    #init thread dictionary
    for i in range(0,11):
        thd[i]=Thread()
    print('\n开始扫描频点 : 88.5 MHz')
    while 1:
        #recv 6bytes from zynq
        data=st.recv(6)
        if(data==b'xxxxxx'):    #clean and reload temp file
            count=0
            rec.close()
            rec=wave.open('fm'+str(state)+'.wav','wb')
            rec.setnchannels(1)
            rec.setsampwidth(2)
            rec.setframerate(16000)
            continue
        #
        dataa=np.array(bytearray(data))
        dataa.dtype='int16'
        #filter
        datab=dataa[2:len(dataa):3]
         #filter
        '''
        datac=dataa[1:len(dataa):3]
        datad=dataa[2:len(dataa):3]
        datae=datab/3+datac/3+datad/3
        datae=datae.astype(int)
        datae.dtype='int16'
        datab=datae[::4]
        '''
        
        count=count+len(datab)
        #声卡播放
        stream.write(data)
        #写缓存文件
        rec.writeframes(bytes(datab))
        #
        if(count>160000):
            count=0
            rec.close()
            if (state>=max_seg): #xiugaide==================================================
                if(thd[state].isAlive()):
                        thd[state].join()
                thd[state]=Thread(target=reco,args=('fm'+str(state)+'.wav',AipSpeech(APP_ID, API_KEY, SECRET_KEY),))
                thd[state].start()
                 #xiugaide==================================================
                if scan==1:
                    now=now+1
                    if(now>=freq_list.size):
                        now=0
                        freq_list=np.array([])
                        cmd.sendto(b'\x00\x00\x05\x00',CMDDST)
                        time.sleep(4)
                        cmd.sendto(b'\x00\x00\x04\x00',CMDDST)
                        time.sleep(4)
                        cmd.sendto(b'\x00\x00\x05\x00',CMDDST)
                        print('\n可疑频点集(MHz):',freq_list)
                        time.sleep(4)
                        cmd.sendto(b'\x00\x00\x03\x00',CMDDST)
                    
                    cmd.sendto((int(freq_list[now]*10)-880).to_bytes(2,'little')+b'\x01\x00',CMDDST)
                    while count<64000:
                        data=st.recv(6)
                        count=count+1
                    count=0
                    for sd in thd:
                        if(thd[sd].isAlive()):
                            thd[sd].join()
                    print('\n开始扫描频点 :'+str(freq_list[now])+'MHz')

                #xiugaide==================================================
                rec=wave.open('fm0.wav','wb')
                rec.setnchannels(1)
                rec.setsampwidth(2)
                rec.setframerate(16000)
                state=0
            else:
                if(thd[state].isAlive()):
                    thd[state].join()
                thd[state]=Thread(target=reco,args=('fm'+str(state)+'.wav',AipSpeech(APP_ID, API_KEY, SECRET_KEY),))
                thd[state].start()
                state=state+1
                rec=wave.open('fm'+str(state)+'.wav','wb')
                rec.setnchannels(1)
                rec.setsampwidth(2)
                rec.setframerate(16000)


def fftp():
     #xiugaide==================================================
    global loc
    global freq_list
     #xiugaide==================================================
    x=[]#fft数据缓存
    time=0#采样次数
    temp_list=[]#临时频点集（计次）
    final_list=np.array([])#临时频点集（计频）
    plt.axis([0, 8192, 0, 500000000])#图标坐标轴
    xz = np.linspace(88, 128, 8192) #X axis data
    ft = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立一个基于TCP的Socket
    ft.connect(('192.168.3.120',10103))
    print('fft connect successful')
    while 1:
        data=ft.recv(4)
        if data==b'\x00\xba\xdc\xfe':
            if(len(x)==8192):
                x=np.array(x)
                 #xiugaide==================================================
                loc=np.where(x>5e7)[0]#寻找过阈值点
                loc=loc/8192*40+88#转化为频率
                loc=np.around(loc,1)#保留小数
                loc=np.unique(loc)#去除重复
                #删除间距过小的点
                for i in range(len(loc)):
                    for j in freq_list:
                        if(abs(loc[i]-j)<0.3):
                            loc[i]=j
                
                final_list=np.append(final_list,loc)
                #
                time=time+1
                if (time>=20):
                    #统计20次采样中出现次数达到一定数量的频点
                    time=0
                    temp_list=list(final_list)
                    final_list=np.unique(final_list)
                    for i in final_list:
                        if(temp_list.count(i)>10):
                            freq_list=np.append(freq_list,i)
                    freq_list=np.unique(freq_list)
                      
                #x=10*np.log10(x)
                 #xiugaide==================================================
                plt.clf()
                plt.xlabel('Frequency/MHz')
                plt.xlim((88,128))
                plt.ylim((0,500000000))
                plt.plot(xz,x)    
                plt.pause(0.01)
            x=[]
        elif data==b'\xaa\xbb\xcc\xdd':#图片显示关闭
            plt.close()
            bufcount=1000#处理掉没处理的数据
            while bufcount:
                data=ft.recv(4)
                bufcount-=1
            x=[]
        else:
            x.append(int.from_bytes(data,'little'))


fmdms=Thread(target=fmdm)
fmdms.start()

ffts=Thread(target=fftp)
ffts.start()
