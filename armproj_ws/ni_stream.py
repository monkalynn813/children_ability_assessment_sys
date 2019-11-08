#!/usr/bin/env python

import numpy as np 
from scipy import signal
import socket
import json
import time
import NIstreamer
from arm_game import gamer
from max_test import calibrator

UDP_IP = "127.0.0.1" 
FILTERED_PORT=5005
RAW_PORT=5003
BUFFER_SIZE=1024
CALIBRATION=[1,0]   
LEFT_SENSOR="Dev1/ai1"
RIGHT_SENSOR="Dev1/ai0"


class signal_processor(object):
    def __init__(self,channels=[RIGHT_SENSOR,LEFT_SENSOR],ni_fs=1000,ref_inx=0):
        savetag='max_test'
        savedir='/home/jingyan/Documents/spring_proj/armproj_ws/data/'
        # savedir='C:\\Users\\pthms\\Desktop\\ling\\children_ability_assessment_sys\\armproj_ws\\data\\'
        self.savepath=savedir+savetag+'.csv'
        
        self.channels=channels
        self.ni_fs=ni_fs
        self.ref_inx=ref_inx
        ######for filter#####
        self.raw_sig_arr=[]
        self.window_size=250
        # self.cutoff_fq=40 #Hz
        #######data networking###
        # self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        self.calibrate=calibrator(self.savepath)
        time.sleep(1.0)
        try:
            self.to_record_arr=[]
            self.now=time.time()
            self.counter=0
            NIstreamer.fake_streaming(channels,self.callback_cali,ni_fs)
            
        except: pass

        self.record_to_file(self.to_record_arr)
        # self.offset=self.calibrate.get_offset()
        # self.max_torque=self.calibrate.get_maximum()
        # self.game=gamer(self.savepath)
        # NIstreamer.fake_streaming(channels,self.callback_game,ni_fs)
        # NIstreamer.fake_streaming(channels,self.callback,ni_fs)
    
    def record_to_file(self,array):
        """
        array=[data,tag,timestamp]
        type(data)==list
        [sensor_data,sensor_data,...]
        tag=str i.e 'reference'
        """
        row=''

        for a in array:
            for d in a[0]: #data
                row+=str(d)
                row+=','
            row+=str(a[1])
            row+=','
            row+=str(a[2])
            row+='\n'
        with open(self.savepath,'a') as f:
            f.write(row)
    
    def callback_cali(self,sample):
        if type(sample)!=list:
            sample=[sample]
      
        if self.counter%37==0:
            self.record_flag,self.tag=self.calibrate.logic(sample)

        if self.record_flag:
            timestamp=time.time()-self.now
            self.to_record_arr.append([sample,self.tag,timestamp])
        self.counter+=1

    def callback_game(self,sample):
        

        if type(sample)!=list:
            sample=[sample]
        raw_torque=[]
        for i in range(len(sample)):
            chn_data=sample[i]-self.offset[i]
            raw_torque.append(CALIBRATION[0]*chn_data)
        

        if len(self.raw_sig_arr)>=self.window_size:
        
            self.game.game_logic(raw_torque,self.max_torque[0]*0.4,self.ref_inx)
        else:
            if len(self.raw_sig_arr)==0:
                print('Please wait for buffering...')
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