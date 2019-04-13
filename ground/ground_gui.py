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
#初始化
APP_ID = '10836826'
API_KEY = 'YvPbyRbqvwt0VDq8RK0GXRxF'
SECRET_KEY = 'GPIvnPuYf33OwSvYYf4bta2YN0HL0SBH'
DST=('192.168.3.120',10101)
CMDDST=('192.168.3.120',10102)
cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #建立一个基于UDP的Socket
 #xiugaide==================================================
CMDDST=('192.168.3.120',10102)
cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #建立一个基于UDP的Socket
loc=[]
freq_list=np.array([88.5,93.7])
current_freq=88.5#dang qian pin lv
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
        result=client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1537,})
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
                f = open('关键词.txt','r',encoding='utf-8-sig')
                liness = f.readlines()#读取文本中全部行
                line_list = []
                for line in liness:
                        line_list.append(line.strip())#line_list为关键词库中关键词的数组集合
                f.close()
                keywords = segStat.iloc[:,0]
                l = len(keywords)
                ciku =[]
                i = 0
                while i<l:
                        if keywords[i] in line_list:
                                ciku.append(keywords[i])
                        i +=1
                times = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                Information_Window.insert("end",'['+str(times)+'频率:'+str(c_freq)+'MHz'+']'+str(lines) + '\n')# 在操作信息窗口显示发送的指令并换行，end为在窗口末尾处显示
                Information_Window.see("end")
                Guanjianci_Window.insert("end",str(segStat) + '\n') # 在操作信息窗口显示发送的指令并换行，end为在窗口末尾处显示
                Guanjianci_Window.see("end") # 此处为显示操作信息窗口进度条末尾内容，以上两行
                m = len(ciku)
                if m > 0:
                        i = 0
                        while i<m:
                                fd=Thread(target=showin,args= (ciku[i],))
                                fd.start()
                                Gj_Window.insert("end",'['+str(times)+'频率:'+str(c_freq)+'MHz'+']'+'搜索到关键词：'+str(ciku[i])+'\n')
                                Gj_Window.see("end")
                                i +=1
        else:
                print(result['err_msg'])
			
def WriteData():
    global DataSend
    global current_freq
    DataSend = EntrySend.get() # 读取当前文本框的内容保存到字符串变量DataSend
    a=DataSend.replace('.','')
    current_freq=(int(a)/10)
    cmd.sendto((int(a)-880).to_bytes(2,'little')+b'\x01\x00',CMDDST)
    
tk.Button(Send, text="设置", command=WriteData).grid(pady=1, sticky=tk.E)
def showin(s):
    tkinter.messagebox.showinfo("提示","搜索到关键词:"+str(s))
def fftp():
    #xiugaide==================================================
    global loc
    global freq_list
    
     #xiugaide==================================================
    ft = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立一个基于TCP的Socket
    ft.connect(('192.168.3.120',10103))
    print('fft connect successful')
    x=[]
    xz = np.linspace(88, 118, 8192) #X axis data
    time=0
    temp_list=[]
    final_list=np.array([])
    while 1:
        data=ft.recv(4)
        if data==b'\x00\xba\xdc\xfe':
            if(len(x)==8192):
                x=np.array(x)
                 #xiugaide==================================================
                loc=np.where(x>4e7)[0]
                loc=loc/8192*40+88
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
                x=10*np.log10(x)
                 #xiugaide==================================================
                plt.figure(2)
                plt.clf()
                plt.xlabel('Frequency/MHz')
                plt.xlim((88,118))
                plt.ylim((30,100))
                plt.plot(xz,np.array(x))    
                plt.pause(0.01)
            x=[]
        elif data==b'\xaa\xbb\xcc\xdd':#图片显示关闭
            plt.close(2)
            bufcount=1000#处理掉没处理的数据
            while bufcount:
                data=ft.recv(4)
                bufcount-=1
            x=[]
        else:
            x.append(int.from_bytes(data,'little'))
            
def fmdm():
    global scan
    global freq_list,now
    global current_freq
    #声卡输出流初始化
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(2),channels = 1,rate = 48000, output = True)
    #网络socket初始化
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立一个基于TCP的Socket
    st.connect(('192.168.3.120',10101))
    print('fmdm connect successful')
    count=0
    state=0
    now = 0
    #缓存文件初始化
    rec=wave.open('fm0.wav','wb')
    rec.setnchannels(1)
    rec.setsampwidth(2)
    rec.setframerate(16000)
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
            rec=wave.open('fm'+str(state)+'.wav','wb')
            rec.setnchannels(1)
            rec.setsampwidth(2)
            rec.setframerate(16000)
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
        #声卡播放
        stream.write(data)
        #写缓存文件
        rec.writeframes(bytes(datab))
        
        if(count>160000):
            count=0
            rec.close()
            nc = int(numberChosen.get())
            dem_time=int(nc/10-1)
            if (state>=dem_time):
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
                        freq_list=np.array([])
                        cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
                        count=0
                        while count<12000:
                            data=st.recv(6)
                            count +=1
                        cmd.sendto(b'\x04\x00\x04\x00',CMDDST)
                        time.sleep(5)
                        cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
                        #print('\n可疑频点集(MHz):',freq_list)
                        time.sleep(5)
                        cmd.sendto(b'\x03\x00\x03\x00',CMDDST)
                    cmd.sendto((int(freq_list[now]*10)-880).to_bytes(2,'little')+b'\x01\x00',CMDDST)
                    count=0
                    while count<64000:
                        data=st.recv(6)
                        count +=1
                    
                    current_freq=freq_list[now]
                    Frequency_Window.delete(0,"end")
                    Frequency_Window.insert("end",'开始扫描频点 :'+str(current_freq)+'MHz')
                
                #xiugaide==================================================
                rec=wave.open('fm0.wav','wb')
                rec.setnchannels(1)
                rec.setsampwidth(2)
                rec.setframerate(16000)
                state=0
            else:
                thd[state]=Thread(target=reco,args=('fm'+str(state)+'.wav',AipSpeech(APP_ID, API_KEY, SECRET_KEY),current_freq,))
                thd[state].start()
                
                if(thd[state+1].isAlive()):
                    thd[state+1].join()
                state += 1
                rec=wave.open('fm'+str(state)+'.wav','wb')
                rec.setnchannels(1)
                rec.setsampwidth(2)
                rec.setframerate(16000)
#按键发送指令
def Open_Serial3():
  cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
  time.sleep(3)
  cmd.sendto(b'\x03\x00\x03\x00',CMDDST)
def Open_Serial4():
  cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
  time.sleep(3)
  cmd.sendto(b'\x04\x00\x04\x00',CMDDST)
def Open_Serial5():
  cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
def Open_Serial6():
  cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
def Open_Serial7():
    global scan,action
    if(1==scan):
        scan=0
        action.configure(text="自动扫描",bg='cornflowerblue')
        tkinter.messagebox.showinfo("提示","以切换为手动扫描模式")
    else:
        scan=1
        action.configure(text= "手动扫描",bg = "red")
        tkinter.messagebox.showinfo("提示","以切换为自动扫描模式")
        
def Open_Serial8():
    cmd.sendto(b'\x06\x00\x06\x00',CMDDST)
fmid=Thread(target=fmdm)
fmid.start()
fftid=Thread(target=fftp)
fftid.start()
tk.Button( switch3, text = "  监  听  ",font = ("宋体",14,"bold"), bd = 4,bg='cornflowerblue',fg="honeydew",command = Open_Serial3 ).pack(side = "left", padx = 5 )
tk.Button( switch3, text = "    停止    ",font = ("宋体",14,"bold"),  bd = 4,bg='red',fg="honeydew",command = Open_Serial5 ).pack(side = "right", padx = 3 )
tk.Button( switch4, text = " 频谱图 ",font = ("宋体",14,"bold"),bd = 4, bg='cornflowerblue',fg="honeydew",command = Open_Serial4 ).pack(side = "left", padx = 5 )
tk.Button( switch4, text = "        退出        ",font = ("宋体",14,"bold"), bd = 4,bg='red',fg="honeydew",command = Open_Serial6 ).pack(side = "right", padx = 5 )
action = tk.Button( switch5,text = "自动扫描", font = ("宋体",14,"bold"),bd = 4,bg='cornflowerblue',fg="honeydew",command = Open_Serial7)
action.pack(side = "left",padx = 5)
tk.Button( switch5,text = "强制退出",font = ("宋体",14,"bold"),bd = 4,bg='red',fg="honeydew",command = Open_Serial8).pack(side = "right", padx = 0.5)
GUI.mainloop()
cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
cmd.sendto(b'\x05\x00\x05\x00',CMDDST)
print('bye bye')
'''problem
line 283 命令无法响应
'''
