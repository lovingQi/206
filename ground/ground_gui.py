import tkinter.messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial.tools.list_ports
import wave
import pyaudio 
import os
import os.path
import codecs
import pandas
import jieba
import socket
import time
import numpy as np
from aip import AipSpeech
from threading import Thread
import matplotlib.pyplot as plt
#=============================
APP_ID = '10836826'
API_KEY = 'YvPbyRbqvwt0VDq8RK0GXRxF'
SECRET_KEY = 'GPIvnPuYf33OwSvYYf4bta2YN0HL0SBH'
FFT_SERVER=('192.168.3.120',10102)
FM_SERVER=('192.168.3.120',10104)
#========================================================
cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #建立一个基于UDP的Socket
CMD_STOP=b'\x05\x00\x05\x00'
CMD_FM=b'\x03\x00\x03\x00'
CMD_FFT=b'\x04\x00\x04\x00'
CMD_KILL=b'\x06\x00\x06\x00'
CMD_NOP=b'\x07\x00\x07\x00'
CMDDST=('192.168.3.120',10105)
 #xiugaide==================================================
loc=[]
freq_list=np.array([88.5])
current_freq=88.5
scan=0
 #xiugaide==================================================
#窗口程序
GUI = tk.Tk()  # 父容器
GUI.title("空中'反黑'智能频谱监测软件")  # 父容器标题
GUI.geometry("1000x600")  # 父容器大小
Information = tk.LabelFrame(GUI, text="广播内容", padx=10, pady=10) # 创建子容器，水平，垂直方向上的边距均为10
Information.place(x=20, y=20)
Information_Window = scrolledtext.ScrolledText(Information, width=112, height=10, padx=10, pady=10,font=("宋体",12),selectforeground='red',wrap=tk.WORD)
Information_Window.grid()
Guanjianci = tk.LabelFrame(GUI, text="关键词统计", padx=10, pady=10)
Guanjianci.place(x=20, y=240)
Guanjianci_Window = scrolledtext.ScrolledText(Guanjianci, width=18, height=17, padx=10, pady=10,font=("宋体",12),wrap=tk.WORD)
Guanjianci_Window.grid()
Gj = tk.LabelFrame(GUI,text = "”黑广播“记录",padx = 10,pady =10)
Gj.place(x=245,y =240)
Gj_Window = scrolledtext.ScrolledText(Gj, width=30, height=17, padx=10, pady=10,font=("宋体",12),fg = "red",wrap=tk.WORD)
Gj_Window.grid()
keyi = tk.LabelFrame(GUI, text="可疑频点列表", padx=10, pady=10)
keyi.place(x=558,y=310)
keyi_Window = scrolledtext.ScrolledText(keyi, width=15, height=12, padx=10, pady=10,font=("宋体",12),fg = "blue",wrap=tk.WORD)
keyi_Window.grid()
Send = tk.LabelFrame(GUI, text="设置中心频率（MHz）", padx=10, pady=5)  
Send.place(x=760, y=310)
DataSend = tk.StringVar()  # 定义DataSend为保存文本框内容的字符串
EntrySend = tk.StringVar()
Send_Window = ttk.Entry(Send, textvariable=EntrySend, width=27)
Send_Window.grid()
#下拉框
xl = tk.LabelFrame(GUI, text="选择单个频点停留时间(s)", padx=10, pady=5)
xl.place(x=760,y=240)
number = tk.StringVar()
numberChosen = ttk.Combobox(xl, width=24, textvariable=number)
numberChosen['values'] = (10, 20, 30, 40, 50,60)     # 设置下拉列表的值
numberChosen.grid()      # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

Frequency = tk.LabelFrame(GUI, text="当前工作状态", padx=10, pady=10)  
Frequency.place(x=558, y=240)
Frequency_Window = ttk.Entry(Frequency,  width=22)
Frequency_Window.grid()

switch3 = tk.LabelFrame( GUI, text = "", padx = 10, pady = 10 )
switch3.place(x = 760, y = 410, width = 220)
switch4 = tk.LabelFrame( GUI, text = "", padx = 10, pady = 10 )
switch4.place(x = 760, y = 460, width = 220)
switch5 = tk.LabelFrame(GUI,text = "",padx = 10,pady = 10)
switch5.place(x = 760, y = 510, width = 220)
#语音识别

def reco(fname,client,c_freq):
    with open(fname, 'rb') as fp:
        try:
            result=client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1537,})
        except:
            print('CLOUD SERVER ERROR')
            result['err_no']=1
        if result['err_no']==0:
                with open ("黑广播.txt",'w',encoding = 'utf-8') as hgb_wb:
                    hgb_wb.write(result['result'][0])
                with open ("黑广播.txt",'r',encoding = 'utf-8') as hgb_wb:
                    lines = hgb_wb.readlines()
                lines = ''.join(lines)
                #切割词组，并过滤停用词
                stoplist = codecs.open('stopwords.txt','r',encoding='utf8').readlines()
                stoplist = set(w.strip() for w in stoplist)#读取停用词表
                segment = []
                segs = jieba.cut(lines)
                segs = [word for word in list(segs) if word not in stoplist]
                for seg in segs:
                        segment.append(seg)
                segments = pandas.DataFrame({
                        '词组':segment
                        })
                c = segments.groupby(by = '词组')['词组'].agg(np.size)
                c = c.to_frame()
                c.columns = ['计数']
                c = c.sort_values(by = ["计数"],ascending = False)#对计数次数排序
                segStat = c.reset_index()#还原segStat矩阵索引
                #关键词提取
                with open('关键词.txt','r',encoding='utf-8-sig') as f:
                    liness = f.read()#读取文本中全部行
                    line_list=liness.split('\n')
                keywords = segStat.iloc[:,0]
                ciku =[]
                for i in keywords:
                        if i in line_list:
                                ciku.append(i)
                times = time.strftime("%m-%d %H:%M:%S",time.localtime())
                Information_Window.insert("end",'['+str(times)+' 频率:'+str(c_freq)+'MHz'+']'+str(lines) + '\n')# 在操作信息窗口显示发送的指令并换行，end为在窗口末尾处显示
                Information_Window.see("end")
                Guanjianci_Window.insert("end",str(segStat) + '\n') # 在操作信息窗口显示发送的指令并换行，end为在窗口末尾处显示
                Guanjianci_Window.see("end") # 此处为显示操作信息窗口进度条末尾内容，以上两行
                for i in ciku:
                    fd=Thread(target=showin,args= (c_freq,))
                    fd.start()
                    Gj_Window.insert("end",'['+str(times)+' 频率:'+str(c_freq)+'MHz'+']'+'\n'+'搜索到关键词：'+str(i)+'\n')
                    Gj_Window.see("end")
        else:
                print(result['err_msg'])
			
def set_freq():
    global DataSend
    global current_freq
    DataSend = EntrySend.get() # 读取当前文本框的内容保存到字符串变量DataSend
    a=DataSend.replace('.','')
    current_freq=(int(a)/10)
    cmd.sendto((int(a)-880).to_bytes(2,'little')+b'\x01\x00',CMDDST)
    

def showin(s):
    root = tk.Tk()
    root.title("提示")
    root.geometry("200x80+600+500")
    l = tk.Label(root,text = '找到“黑广播”',font = ("宋体",12))
    r = tk.Label(root,text = '频率：'+str(s),font = ("宋体",14),fg='red')
    tm = tk.Label(root,fg='blue', anchor = 'w')
    tm.place(x=1, y= 60, width =150 )
    l.place(x = 50,y =10)
    r.place(x = 50, y =30)
    def autoclose():
        for i in range(6):
            tm['text'] = '距离窗口关闭还有{}秒'.format(6-i)
            time.sleep(1)
        root.destroy()
    t = Thread(target = autoclose )
    t.start()
    root.mainloop()
def fftp():
    #xiugaide==================================================
    global loc
    global freq_list
     #xiugaide==================================================
    ft = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立一个基于TCP的Socket
    try_count=0
    while 1:
        try:
            ft.connect(FFT_SERVER)
            break
        except:
            print('FFT CONNECT ERROR ....RETRY!',try_count)
            try_count+=1
            if(try_count>5):
                print('FFT CONNECT ERROR')
                exit()
    print('fft connect successful')
    x=[]
    xz = np.linspace(88, 144, 8192) #X axis data
     #xz = np.linspace(88, 128, 8192) #X axis data
    time=0
    temp_list=[]
    final_list=np.array([])
    
    FIGURE_HEAD=b'\x00\xba\xdc\xfe'
    FIGURE_CLOSE=b'\xaa\xbb\xcc\xdd'
    while 1:
        data=ft.recv(4)
        if data==FIGURE_HEAD:
            if(len(x)==8192):
                x=np.array(x)
                 #xiugaide==================================================
                loc=np.where(x>2e7)[0]
                loc=loc/8192*56+88
                loc=np.around(loc,1)
                loc=np.unique(loc)

                for i in range(len(loc)):
                    for j in freq_list:
                        if(abs(loc[i]-j)<0.4):
                            loc[i]=j
                
                final_list=np.append(final_list,loc)
                time=time+1
                if (time>=20):
                    time=0
                    temp_list=list(final_list)
                    final_list=np.unique(final_list)
                    for i in final_list:
                        if(temp_list.count(i)>10):
                            freq_list=np.append(freq_list,i)
                    freq_list=np.unique(freq_list)
                    l = len(freq_list)
                    i = 0
                    keyi_Window.delete(0.1,"end")
                    while i<l:
                        keyi_Window.insert("end",str(freq_list[i])+'\n')
                        i +=1
                x=20*np.log10(x)
                 #xiugaide==================================================
                plt.figure(2)
                plt.clf()
                plt.xlabel('Frequency/MHz')
                #plt.xlim((88,128))
                plt.xlim((88,144))
                plt.ylim((60,200))
                plt.plot(xz,np.array(x))    
                plt.pause(0.01)
            x=[]
            
        elif data==FIGURE_CLOSE:#图片显示关闭
            plt.close(2)
            x=[]
        else:
            x.append(int.from_bytes(data,'little'))
#========================================================            
def change_freq():
    cmd.sendto(CMD_STOP,CMDDST)
    time.sleep(2)
    cmd.sendto(CMD_FFT,CMDDST)
    time.sleep(5)
    cmd.sendto(CMD_STOP,CMDDST)
    time.sleep(3)
    cmd.sendto(CMD_FM,CMDDST)
    
#========================================================
def fmdm():
    global scan
    global freq_list,now
    global current_freq
    #声卡输出流初始化
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(2),channels = 1,rate = 48000, output = True)
    except:
        print('OPEN SOUND DEVICE ERROR')
        exit()
    #网络socket初始化
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立一个基于TCP的Socket
    try_count=0
    while 1:
        try:
            st.connect(FM_SERVER)
            break
        except:
            print('FM CONNECT ERROR ....RETRY!',try_count)
            try_count+=1
            if(try_count>5):
                print('FM CONNECT ERROR')
                exit()
        
    print('fm connect success')
    count=0
    state=0
    now = 0
    #缓存文件初始化
    try:
        rec=wave.open('fm0.wav','wb')
        rec.setnchannels(1)
        rec.setsampwidth(2)
        rec.setframerate(16000)
    except:
        print('WAVFILE OPEN ERROR!')
    #线程字典及初始化
    thd={} 
    tt=0
    for i in range(0,11):
        thd[i]=Thread()
    while 1:
        data=st.recv(6)
        if(data==b'xxxxxx'):
            count=0
            rec.close()
            try:
                rec=wave.open('fm0.wav','wb')
                rec.setnchannels(1)
                rec.setsampwidth(2)
                rec.setframerate(16000)
            except:
                print('WAVFILE OPEN ERROR!')
            continue
        dataa=np.array(bytearray(data))
        dataa.dtype='int16'
        #平滑滤波
        datab=dataa[0:len(dataa):3]
        datac=dataa[1:len(dataa):3]
        datad=dataa[2:len(dataa):3]
        datae=datab/3+datac/3+datad/3
        datae=datae.astype(int)
        datae.dtype='int16'
        datab=datae[::4]
        count=count+len(datab)
        
        try:
            #声卡播放
            stream.write(data)
            #写缓存文件
            rec.writeframes(bytes(datab))
        except:
            print('STREAM WRITE ERROR')
        
        if(count>160000):
            count=0
            rec.close()
            nc = int(numberChosen.get())
            dem_time=int(nc/10-1)
            if (~(state<dem_time)):
                if(thd[state].isAlive()):
                    thd[state].join()
                thd[state]=Thread(target=reco,args=('fm'+str(state)+'.wav',AipSpeech(APP_ID, API_KEY, SECRET_KEY),current_freq,))
                thd[state].start()
                 #xiugaide==================================================
                if(1==scan):
                    now += 1
                    with open ("黑广播.txt",'w',encoding = 'utf-8') as hgb_wb:
                        hgb_wb.truncate()
                    if(now>=freq_list.size):
                        now=0
                        for sd in thd:
                            if(thd[sd].isAlive()):
                                thd[sd].join()
                        freq_list=np.array([88.5])                    
                        cg=Thread(target=change_freq,)
                        cg.start()
                        while(cg.isAlive()):
                            data=st.recv(6)
                    cmd.sendto((int(freq_list[now]*10)-880).to_bytes(2,'little')+b'\x01\x00',CMDDST)                            
                    count=16000
                    while count>0:
                        data=st.recv(6)
                        count -=1
                    current_freq=freq_list[now]
                Frequency_Window.delete(0,"end")
                Frequency_Window.insert("end",'开始扫描频点 :'+str(current_freq)+'MHz')
                #xiugaide==================================================
                try:
                    rec=wave.open('fm0.wav','wb')
                    rec.setnchannels(1)
                    rec.setsampwidth(2)
                    rec.setframerate(16000)
                    state=0
                except:
                    print('FAIL TO OPEN WAVFILE!')
            else:
                if(thd[state].isAlive()):
                    thd[state].join()
                thd[state]=Thread(target=reco,args=('fm'+str(state)+'.wav',AipSpeech(APP_ID, API_KEY, SECRET_KEY),current_freq,))
                thd[state].start()
                state += 1
                try:
                    rec=wave.open('fm0.wav','wb')
                    rec.setnchannels(1)
                    rec.setsampwidth(2)
                    rec.setframerate(16000)
                except:
                    print('FAIL TO OPEN WAVFILE!')
                    
#按键发送指令
def start_fm():
    cmd.sendto(CMD_FM,CMDDST)
def start_fft():
    cmd.sendto(CMD_FFT,CMDDST)
def stop_datatran():
    cmd.sendto(CMD_STOP,CMDDST)
def reserve():
    cmd.sendto(CMD_NOP,CMDDST)
def kill_server():
    cmd.sendto(CMD_KILL,CMDDST)
def scan_switch():
    global scan,action
    if(1==scan):
        scan=0
        action.configure(text="开始扫描",bg='cornflowerblue')
    else:
        scan=1
        action.configure(text= "停止扫描",bg = "red")
        
tk.Button(Send, text="设置", command=set_freq).grid(pady=1, sticky=tk.E)
tk.Button( switch3, text = " 解 调  ",font = ("宋体",14,"bold"), bd = 4,bg='cornflowerblue',fg="honeydew",command = start_fm ).pack(side = "left", padx = 5 )
tk.Button( switch3, text = "    停止    ",font = ("宋体",14,"bold"),  bd = 4,bg='red',fg="honeydew",command = stop_datatran ).pack(side = "right", padx = 3 )
tk.Button( switch4, text = " 频谱图 ",font = ("宋体",14,"bold"),bd = 4, bg='cornflowerblue',fg="honeydew",command = start_fft ).pack(side = "left", padx = 5 )
tk.Button( switch4, text = "        退出        ",font = ("宋体",14,"bold"), bd = 4,bg='red',fg="honeydew",command = reserve ).pack(side = "right", padx = 5 )
action = tk.Button( switch5,text = "开始扫描", font = ("宋体",14,"bold"),bd = 4,bg='cornflowerblue',fg="honeydew",command = scan_switch)
action.pack(side = "left",padx = 5)
tk.Button( switch5,text = "强制退出",font = ("宋体",14,"bold"),bd = 4,bg='red',fg="honeydew",command = kill_server).pack(side = "right", padx = 0.5)

try:
    fmid=Thread(target=fmdm)
    fmid.start()
    fftid=Thread(target=fftp)
    fftid.start()
except:
    print('COULD NOT CREATE MAIN THREAD!')
    exit(0)

GUI.mainloop()

cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
exit(0)
