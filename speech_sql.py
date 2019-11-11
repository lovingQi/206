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
import pymysql
import numpy as np

from aip import AipSpeech
from threading import Thread
#初始化
sql_pwd='lizuguang'
sql_usr='lizuguang'
sql_host='127.0.0.1'

APP_ID = '15628658'
API_KEY = 'GAy9qAeG8BB5avZPWzeKzt5Y'
SECRET_KEY = '7B4gXiXLpfnHH4AXBUjiO04nphyEgGBp'

HOST_ADDR='192.168.3.120'
DST=(HOST_ADDR,10101)
CMDDST=(HOST_ADDR,10102)
CMD_STOP=b'\x00\x00\x05\x00'
CMD_FFT=b'\x00\x00\x04\x00'
CMD_DM=b'\x00\x00\x03\x00'

SIG_FFTDATA_END=b'\x00\xba\xdc\xfe'
SIG_PIC_CLOSE=b'\xaa\xbb\xcc\xdd'
SIG_DM_SAVE=b'xxxxxx'

cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #建立一个基于UDP的Socket
loc=[]
freq_list=np.array([102.5])
current_freq=102.5       #当前频点初始化
scan=0
n = 0
#================清空数据库===================================
db = pymysql.connect(
    host = sql_host,
    user = sql_usr,  password = sql_pwd,
    database = 'speech',
    charset = "utf8")
#使用cursor()方法创建一个游标对象cursor
cur = db.cursor()
'''sql = "INSERT INTO doubtful_freq_list values(24);"
print(cur.execute(sql))'''
sql = "delete doubtful_freq_list from doubtful_freq_list"
cur.execute(sql)
sql = "delete illegal_freq from illegal_freq"
cur.execute(sql)
sql = "delete now_list_freq from now_list_freq"
cur.execute(sql)
sql = "delete voice_text from voice_text"
cur.execute(sql)
cur.close()
db.close()
with open ("C:\\inetpub\\wwwroot\\Data\\now_freq.txt",'w',encoding = 'utf-8') as now_freq_w:
    now_freq_w.truncate()       #清除now_freq.txt中的当前频点，即初始化为空
#语音识别
def reco(fname,client,c_freq):
    #====================连接数据库==============================
    db = pymysql.connect(
    host = sql_host,
    user = sql_usr,  password = sql_pwd,
    database = 'speech',
    charset = "utf8")
    #使用cursor()方法创建一个游标对象cursor
    cur = db.cursor()
    #=========================================================
    with open(fname, 'rb') as fp:
        result=client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1537,})
        if result.get('err_no')==0:
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
                f = open('keywords.txt','r',encoding='utf-8-sig')
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
                                ciku.append(str(keywords[i]))
                        i +=1
                #sql = "UPDATE voice_text SET frequency = %s,text = '%s' WHERE id = 0" %(c_freq,str(lines))#更新文本内容
                sql = "SELECT * FROM voice_text"
                cur.execute(sql)
                results = cur.fetchall()
                if(len(results)>10):
                    sql = "DELETE voice_text FROM voice_text"
                    cur.execute(sql)
                sql = "INSERT INTO voice_text(frequency,text) values(%s,'%s')"%(c_freq,str(lines))
                cur.execute(sql)
                m = len(ciku)
                sql = "SELECT * FROM illegal_freq"
                cur.execute(sql)
                results = cur.fetchall()
                if(len(results)>10):
                    sql = "DELETE illegal_freq FROM illegal_freq"
                    cur.execute(sql)
                for i in range(m):
                    sql = "insert into illegal_freq(frequency,keyword) values(%s,%s)"
                    cur.execute(sql,[float(c_freq),ciku[i]])
                    #cur.executemany(sql,[(c_freq,ciku[i]) for i in range(m)])
        else:
                print(result.get('err_msg'))
    cur.close()
    db.close()
def fftp():
    global loc
    global freq_list
    ydata = []
    db = pymysql.connect(
    host = sql_host,
    user = sql_usr,  password = sql_pwd,
    database = 'speech',
    charset = "utf8")
    cur = db.cursor()
    FM_list = [ '87.6','88.7', '90.0','90.5','91.5','93.1','96.6', '97.4', '99.6',  '100.6', '101.8', '102.5', '103.9', '106.1', '106.6', '107.3']
    ft = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立一个基于TCP的Socket
    ft.connect((HOST_ADDR,10103))
    print('fft connect successful')
    x=[]
    time1=0
    temp_list=[]
    final_list=np.array([])
    while 1:
        data=ft.recv(4)
        '''try:
            with open("C:\\inetpub\\wwwroot\\Data\\now_freq.txt",'w',encoding = 'utf-8') as now_freq_write:
                now_freq_write.truncate()       #清除now_freq.txt中的当前频点，即初始化为空
        except:
            print('now_freq.txt open fail')'''
        if data==SIG_FFTDATA_END:
            if(len(x)==8192):
                x=np.array(x)
                loc=np.where(x[:4096]>3e7)[0]          #loc为频谱数据x>2e7的位置
                loc=loc/8192*40+88
                loc=np.around(loc,1)
                loc=np.unique(loc)
                for i in range(len(loc)):
                    for j in freq_list:
                        if(abs(loc[i]-j)<0.4):
                            loc[i]=j
                final_list=np.append(final_list,loc)
                time1=time1+1
                if (time1>=20):
                    time1=0
                    temp_list=list(final_list)
                    final_list=np.unique(final_list)
                    for i in final_list:
                        if(temp_list.count(i)>10):
                            freq_list=np.append(freq_list,i)
                    freq_list=np.unique(freq_list)
                    sql = "DELETE doubtful_freq_list FROM doubtful_freq_list"
                    cur.execute(sql)
                    for i in range(len(freq_list)):
                        if str(freq_list[i]) not in FM_list:                                  #判断是否在正常广播集合中
                            sql = "INSERT INTO doubtful_freq_list values(%s)"%(float(freq_list[i]))
                            cur.execute(sql)
                            keyi_list = np.array([])
                            keyi_list = np.append(keyi_list, freq_list[i])
                            freq_list = np.delete(freq_list, i, axis = 0)
                            freq_list = np.insert(freq_list, 0 , keyi_list)
                    sql = "DELETE now_list_freq FROM now_list_freq"
                    cur.execute(sql)
                    sql = "INSERT INTO now_list_freq values(%s,%s)"
                    cur.executemany(sql,[(float(freq_list[i]),i) for i in range(len(freq_list))])
                ydata = x[0:4096:2]
                ydata = 10*np.log10(ydata)
                try:
                    with open("C:\\inetpub\\wwwroot\\Data\\data.txt",'w',encoding='utf-8') as freqplot_data_write:
                        for i in range(2048):
                            freqplot_data_write.writelines(str(round(ydata[i],2)))
                            freqplot_data_write.write(',')
                except:
                    print('频谱数据写入data.txt文件通道被占用')
            x=[]
        elif data==SIG_PIC_CLOSE:     #图片显示关闭
            #处理掉没处理的数据
            for i in range(1000):
                data=ft.recv(4)
            x=[]
        else:
            x.append(int.from_bytes(data,'little'))
    cur.close()
    db.close()  
def change_freq():
    cmd.sendto(CMD_STOP,CMDDST)#
    time.sleep(2)
    cmd.sendto(CMD_FFT,CMDDST)#
    time.sleep(5)
    cmd.sendto(CMD_STOP,CMDDST)#
    time.sleep(3)
    cmd.sendto(CMD_DM,CMDDST)#
def fmdm():
    global scan
    global freq_list,now
    global current_freq
    global scan_time
    #声卡输出流初始化
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(2),channels = 1,rate = 48000, output = True)
    #网络socket初始化
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立一个基于TCP的Socket
    st.connect((HOST_ADDR,10101))
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
        current2_freq = current_freq
        if(data==SIG_DM_SAVE):
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
        count=count+len(datab)
        #声卡播放
        stream.write(data)
        #写缓存文件
        rec.writeframes(bytes(datab))
        if(count>160000):
            count=0
            rec.close()
            dem_time=int(scan_time/10-1)
            if (state>=dem_time):
                if(thd[state].isAlive()):
                    thd[state].join()
                thd[state]=Thread(target=reco,args=('fm'+str(state)+'.wav',AipSpeech(APP_ID, API_KEY, SECRET_KEY),current2_freq,))
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
                        freq_list=np.array([102.5])                    
                        cg=Thread(target=change_freq,)
                        cg.start()
                        while(cg.isAlive()):
                            data=st.recv(6)
                    cmd.sendto((int(freq_list[now]*10)-880).to_bytes(2,'little')+b'\x01\x00',CMDDST)
                    current_freq=freq_list[now]
                    with open("C:\\inetpub\\wwwroot\\Data\\now_freq.txt",'w',encoding='utf-8') as now_freq_write:
                        now_freq_write.write(str(current_freq))
                    '''sql = "DELETE now_freq FROM now_freq"
                    cur.execute(sql)
                    sql = "insert into now_freq values(%s)"
                    cur.execute(sql,[float(current_freq)])'''
                    while count<16000:
                        data=st.recv(6)
                        count +=1
                    count=0
                rec=wave.open('fm0.wav','wb')
                rec.setnchannels(1)
                rec.setsampwidth(2)
                rec.setframerate(16000)
                state=0
            else:
                thd[state]=Thread(target=reco,args=('fm'+str(state)+'.wav',AipSpeech(APP_ID, API_KEY, SECRET_KEY),current2_freq,))
                thd[state].start()
                
                if(thd[state+1].isAlive()):
                    thd[state+1].join()
                state += 1
                rec=wave.open('fm'+str(state)+'.wav','wb')
                rec.setnchannels(1)
                rec.setsampwidth(2)
                rec.setframerate(16000)
        '''cur.close()
        db.close()'''
#========查询数据库scan和 scan_time的值，判断是否执行扫描,及查询扫描时间============
def scan_sql():
    global scan                  #scan扫描指令，1扫描；0停止扫描
    global freq_list
    global scan_time        #scan_time为扫描停留时间：0（初始值）;扫描时可选10s:80s:10s
    global current_freq
    scan_time = 0
    scanl=0
    while 1:                        #循环查询数据库中 scan 和 scan_time的值
        db = pymysql.connect(
        host = sql_host,
        user = sql_usr,  password = sql_pwd,
        database = 'speech',
        charset = "utf8")
        cur = db.cursor()
        sql = "SELECT * FROM scan"
        cur.execute(sql)
        results = cur.fetchall()
        scan = results[0][0]
        sql = "SELECT * FROM scan_time"
        cur.execute(sql)
        result = cur.fetchall()
        scan_time = result[0][0]

        if(scanl!=scan):
            print('empty')
            freq_list=np.array([102.5])
            sql = "DELETE doubtful_freq_list FROM doubtful_freq_list"
            cur.execute(sql)
            sql = "DELETE now_list_freq FROM now_list_freq"
            cur.execute(sql)
        scanl=scan
        lines=''
        try:
            size = os.path.getsize("C:\\inetpub\\wwwroot\\Data\\now_freq.txt")
            if size != 0:
                with open("C:\\inetpub\\wwwroot\\Data\\now_freq.txt",'r',encoding='utf-8') as now_freq_read:
                    lines=now_freq_read.readlines()
                    current_freq=float(lines[0])
        except:
            print('get current_freq fail')
        cur.close()
        db.close()
        
#=================================================================
fmid=Thread(target=fftp)
fmid.start()
fftid=Thread(target=fmdm)
fftid.start()
scan_sqls = Thread(target=scan_sql)
scan_sqls.start()
#========防止data.txt文件被破坏====================================
#open("C:\\inetpub\\wwwroot\\Data\\data.txt",'w',encoding='utf-8').close()
cmd.sendto(CMD_STOP,CMDDST)
