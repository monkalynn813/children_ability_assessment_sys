#!/usr/bin/env python

import numpy as np 
from scipy import signal
import socket
import json
import time
import NIstreamer
import matplotlib.pyplot as plt


UDP_IP = "127.0.0.1" 
FILTERED_PORT=5002
RAW_PORT=5003
BUFFER_SIZE=1024
CALIBRATION=[1,0]

class signal_processor(object):
    def __init__(self,mode='run',channels=["Dev1/ai0","Dev1/ai1"],ni_fs=1000):
        self.channels=channels
        self.ni_fs=ni_fs
        ######for filter#####
        self.raw_sig_arr=[]
        self.window_size=250
        self.cutoff_fq=2 #Hz
        #######data networking###
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        if mode=='run':
            callback=self.game
        if mode=='raw':
            self.fig=plt.figure()
            self.ax=self.fig.add_subplot(111)
            self.fig.show()
            self.i=0
            callback=self.raw_torque
        if mode=='filter':
            callback=self.filter_lp
        
        NIstreamer.start_streaming(channels,callback,ni_fs)
    
    def raw_torque(self,sample):
        raw_torque=[]
        for k in range(len(self.channels)):
            raw_torque.append(CALIBRATION[0]*sample[k]+CALIBRATION[1])
        

    def filter_lp(self,sample):
        
        if len(self.raw_sig_arr)>=self.window_size and len(self.raw_sig_arr) %1==0:
            self.raw_sig_arr=self.raw_sig_arr[-self.window_size:]

            raw_sig_matrix=np.array(self.raw_sig_arr)
            filtered_data_allchn=[]
            for k in range(len(self.channels)):
                channel_raw=raw_sig_matrix[:,k]
                channel_filtered=lowpass(self.cutoff_fq,channel_raw,self.ni_fs)
                filtered_data_allchn.append(channel_filtered)
            
            print(filtered_data_allchn)
        self.raw_sig_arr.append(sample) 
    def game(self,sample):
        
        if len(self.raw_sig_arr)>=self.window_size and len(self.raw_sig_arr) %1==0:
            self.raw_sig_arr=self.raw_sig_arr[-self.window_size:]

            raw_sig_matrix=np.array(self.raw_sig_arr)
            filtered_data_allchn=[]
            for k in range(len(self.channels)):
                channel_raw=raw_sig_matrix[:,k]
                channel_filtered=lowpass(self.cutoff_fq,channel_raw,self.ni_fs)
                filtered_data_allchn.append(channel_filtered)
            
            
        self.raw_sig_arr.append(sample)        
  
######helper function###############
def lowpass(cutoff,data,fs,order=5):
    nyq=0.5*fs
    normal_cutoff=cutoff/nyq
    b, a = signal.butter(order, normal_cutoff, btype='low',analog=False)
    return signal.lfilter(b, a, data, axis=0)

def main():
        signal_processor()    

if __name__ == '__main__':
	main()