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
        self.sock_raw = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock_raw.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock_raw.bind((UDP_IP,RAW_PORT))

        self.sock_flag = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock_flag.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock_flag.bind((UDP_IP,FLAG_PORT))

        if mode=='plot':
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
            
            raw_torque=[]
            for chn_data in data:
                raw_torque.append(CALIBRATION[0]*chn_data+CALIBRATION[1])

            if i%10==0:
                x.append(i)
                y.append(raw_torque)
                if len(y)>200:
                    y=y[-200:]
                    x=x[-200:]
                
                ax.plot(x,y,color='b')
                fig.canvas.draw()
                ax.set_xlim(left=max(0, i-100), right=i+100)
            i+=1
        plt.close()

    def record_raw(self):
        while True:
            data,addr=self.sock_raw.recvfrom(BUFFER_SIZE)
            data=json.loads(data)
            flag,addr_=self.sock_flag.recvfrom(BUFFER_SIZE)
            flag=json.loads(flag)
            
            # if flag:
                #write in CSV file

raw_recorder(mode='plot')