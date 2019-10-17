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

    def interface(self):
        ui=gamer()
        maxtorque=1
        threshold=0.4*maxtorque
        while True:
            data,addr=self.sock_filter.recvfrom(BUFFER_SIZE)
            data=json.loads(data)
            

            ui.game_logic(data,threshold)



user_interface(mode='run')
