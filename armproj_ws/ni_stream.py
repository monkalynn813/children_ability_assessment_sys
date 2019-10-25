#!/usr/bin/env python

import numpy as np 
from scipy import signal
import socket
import json
import time
import NIstreamer
from arm_game import gamer


UDP_IP = "127.0.0.1" 
FILTERED_PORT=5005
RAW_PORT=5003
BUFFER_SIZE=1024
CALIBRATION=[1,0]   
LEFT_SENSOR="Dev1/ai1"
RIGHT_SENSOR="Dev1/ai0"


class signal_processor(object):
    def __init__(self,channels=[RIGHT_SENSOR,LEFT_SENSOR],ni_fs=1000,ref_inx=0):
        savetag='test_record001'
        savedir='/home/jingyan/Documents/spring_proj/armproj_ws/data/'
        self.savepath=savedir+savetag+'.csv'
        
        self.channels=channels
        self.ni_fs=ni_fs
        self.ref_inx=ref_inx
        ######for filter#####
        self.raw_sig_arr=[]
        self.window_size=250
        self.cutoff_fq=40 #Hz
        #######data networking###
        # self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.game=gamer(self.savepath)
        NIstreamer.start_streaming(channels,self.callback,ni_fs)
        # NIstreamer.fake_streaming(channels,self.callback,ni_fs)
    
    def callback(self,sample):
        if type(sample)!=list:
            sample=[sample]
        raw_torque=[]
        for chn_data in sample:
            raw_torque.append(CALIBRATION[0]*chn_data+CALIBRATION[1])
        
        # if len(self.raw_sig_arr)>=self.window_size and len(self.raw_sig_arr) %1==0:
        #     self.raw_sig_arr=self.raw_sig_arr[-self.window_size:]

        #     raw_sig_matrix=np.array(self.raw_sig_arr)
        #     filtered_data_allchn=[]
        #     for k in range(len(self.channels)):
        #         channel_raw=raw_sig_matrix[:,k]
        #         channel_filtered=lowpass(self.cutoff_fq,channel_raw,self.ni_fs)
        #         filtered_data_allchn.append(channel_filtered[-1])
            
            # msg=json.dumps(raw_torque).encode() #ATTENTION: raw torque is one data point ahead of the filtered data
            # self.sock.sendto(msg,(UDP_IP,RAW_PORT))
            # msg=json.dumps(filtered_data_allchn).encode()
            # self.sock.sendto(msg,(UDP_IP,FILTERED_PORT))
        self.game.game_logic(raw_torque,2.0,self.ref_inx)
        # elif len(self.raw_sig_arr)==0:
        #     print('Please wait for buffering...')
        # elif len(self.raw_sig_arr)==self.window_size-1:
        #     print('Start streaming...')


        
        self.raw_sig_arr.append(raw_torque) 



######helper function###############
def lowpass(cutoff,data,fs,order=5):
    nyq=0.5*fs
    normal_cutoff=cutoff/nyq
    b, a = signal.butter(order, normal_cutoff, btype='low',analog=False)
    return signal.lfilter(b, a, data, axis=0)


def main():
    signal_processor(ni_fs=1000)    

if __name__ == '__main__':
	main()