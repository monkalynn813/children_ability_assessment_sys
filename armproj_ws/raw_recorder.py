#!/usr/bin/env python

import numpy as np 
from scipy import signal
import socket
import json
import time
import matplotlib.pyplot as plt


UDP_IP = "127.0.0.1" 
FLAG_PORT=5004
RAW_PORT=5003
BUFFER_SIZE=1024
CALIBRATION=[1,0]    


class raw_recorder(object):
    def __init__(self,mode='record'):
        savetag='test_record001'
        savedir='/home/jingyan/Documents/spring_proj/armproj_ws/data/'
        self.savepath=savedir+savetag+'.csv'
        self.delim=','

        self.sock_raw = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock_raw.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock_raw.bind((UDP_IP,RAW_PORT))

        self.sock_flag=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock_flag.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock_flag.bind((UDP_IP,FLAG_PORT))

        if mode=='test':
            self.plot_raw()
        if mode=='record':
            self.record_raw()

    def plot_raw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.show()

        i = 0
        x, y = [], []

        while True:
            data,addr=self.sock_raw.recvfrom(BUFFER_SIZE)
            data=json.loads(data)
            
            
            if i%1==0:
                x.append(i)
                y.append(data)
                if len(y)>500:
                    y=y[-500:]
                    x=x[-500:]
                
                ax.plot(x,y,color='b')
                fig.canvas.draw()
                ax.set_xlim(left=max(0, i-600), right=i+600)
            i+=1
        plt.close()

    def record_raw(self):
        while True:
            data,addr=self.sock_raw.recvfrom(BUFFER_SIZE)
            data=json.loads(data)


            flag,addr_=self.sock_flag.recvfrom(BUFFER_SIZE)
            flag=json.loads(flag)
            
            try:
                if len(flag)>1 and flag[0]:
                    tag=flag[1]
                    row=''
                    row+=str(tag)
                    row+=self.delim
                    for t in data:
                        row+=str(t)
                        row+=self.delim
                    row+='\n'
                    with open(self.savepath,'a') as f:
                        f.write(row)
            except:
                continue

                
raw_recorder(mode='test')