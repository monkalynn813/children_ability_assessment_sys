#!/usr/bin/env python

import numpy as np 
from scipy import signal
import socket
import json
import time
import NIstreamer

UDP_IP = "127.0.0.1" 
FILTERED_PORT=5002
RAW_PORT=5003
BUFFER_SIZE=1024
CALIBRATION=[1,0]

class signal_processor(object):
    def __init__(self,channels,ni_fs):
        self.channels=channels
        self.ni_fs=ni_fs
        ######for filter#####
        self.raw_sig_arr=[]
        self.window_size=250
        self.cutoff_fq=2 #Hz
        #######data networking###
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        NIstreamer.start_streaming(channels,self.callback,ni_fs)
    def callback(self,sample):
        #####send raw torque to raw_port###########
        raw_toque=CALIBRATION[0]*
        
    




        



    def filter_lp(self,sample):
        if len(self.raw_sig_arr)>=self.window_size and len(self.raw_sig_arr) %1==0:
            self.raw_sig_arr=self.raw_sig_arr[-self.window_size:]

            raw_sig_matrix=np.array(self.raw_sig_arr)
            filtered_data_allchn=[]
            for k in range(len(self.channels)):
                channel_raw=raw_sig_matrix[:,k]
                channel_filtered=lowpass(self.cutoff_fq,channel_raw,self.ni_fs)
                filtered_data_allchn.append(channel_filtered)
            
        self.raw_sig_arr.append(sample)

def lowpass(cutoff,data,fs,order=5):
    nyq=0.5*fs
    normal_cutoff=cutoff/nyq
    b, a = signal.butter(order, normal_cutoff, btype='low',analog=False)
    return signal.lfilter(b, a, data, axis=0)

def main():
        streamer()    

if __name__ == '__main__':
	main()