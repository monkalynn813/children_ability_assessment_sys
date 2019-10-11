#!/usr/bin/env python

import numpy as np 
import socket
import json
import time
import matplotlib.pyplot as plt
from  arm_game import gamer


UDP_IP = "127.0.0.1" 
FLAG_PORT=5004
FILTERED_PORT=5005
BUFFER_SIZE=1024
CALIBRATION=[1,0]    

class user_interface(object):
    def __init__(self,mode='run'):
        self.sock_filter=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock_filter.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock_filter.bind((UDP_IP,FILTERED_PORT))

        self.sock_flag=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        if mode=='test':
            self.filter_plot()
        if mode=='run':
            self.interface()
        
    def filter_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.show()

        i = 0
        x, y = [], []

        while True:
            data,addr=self.sock_filter.recvfrom(BUFFER_SIZE)
            data=json.loads(data)
            
            filter_torque=[]
            for chn_data in data:
                filter_torque.append(CALIBRATION[0]*chn_data+CALIBRATION[1])

            if i%10==0:
                x.append(i)
                y.append(filter_torque)
                if len(y)>200:
                    y=y[-200:]
                    x=x[-200:]
                
                ax.plot(x,y,color='b')
                fig.canvas.draw()
                ax.set_xlim(left=max(0, i-100), right=i+100)
            i+=1
        plt.close()

    def interface(self):
        ui=gamer()
        while True:
            data,addr=self.sock_filter.recvfrom(BUFFER_SIZE)
            data=json.loads(data)
            
            filter_torque=[]
            for chn_data in data:
                filter_torque.append(CALIBRATION[0]*chn_data+CALIBRATION[1])

            ui.game_logic(filter_torque)



user_interface(mode='test')
