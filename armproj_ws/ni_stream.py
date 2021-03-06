#!/usr/bin/env python

import numpy as np 
import time
from NIstreamer import *
from arm_game import gamer
from max_test import calibrator
import warnings
import copy

CALIBRATION=[53,51.9] ##Modl [77(RIGHT),76(LEFT)]
LEFT_SENSOR="Dev1/ai1"
RIGHT_SENSOR="Dev1/ai0"


class signal_processor(object):
    def __init__(self,channels=[RIGHT_SENSOR,LEFT_SENSOR],ni_fs=1000,ref_inx=0):
        """
        channels: list of string that indicates which port to read
        ni_fs: sampling rate
        ref_inx: index number for the channel list of which arm is the reference arm
        """
        savetag_cali='demo_cali1203v2'
        savetag_game='demo_game1203v2'
        # savedir='/home/jingyan/Documents/spring_proj/armproj_ws/data/'
        savedir='C:\\Users\\pthms\\Desktop\\ling\\children_ability_assessment_sys\\armproj_ws\\data\\'
        self.savepath_cali=savedir+savetag_cali+'.csv'
        self.savepath_game=savedir+savetag_game+'.csv'
        
        self.channels=channels
        self.ni_fs=ni_fs
        self.ref_inx=ref_inx

        render_fps=27
        self.render_lag=int(ni_fs/render_fps)

        self.pre_exp=calibrator(self.ref_inx,self.savepath_cali)
        
        self.to_record_arr=[]
        self.counter=0
        self.record_flag=False
        self.now=time.time()
        try:
            NI=ni_stream('max_test')
            NI.start_streaming(channels,self.callback_cali,ni_fs)
            # NIstreamer.fake_streaming(channels,self.callback_cali,ni_fs)
            
        except: pass

        NI.stop_streaming()
        self.offset=self.pre_exp.get_offset()
        print('offset:',self.offset)
        push_arr=[]
        pull_arr=[]
        
        for i in range(len(self.to_record_arr)):
            sample=self.to_record_arr[i][0]
            tag=self.to_record_arr[i][1]
            timestamp=self.to_record_arr[i][2]

            ##calibration: convert to torque
            sample[0]-=self.offset[0]
            sample[1]-=self.offset[1]
            sample[0]*=CALIBRATION[0]
            sample[1]*=CALIBRATION[1]

            ##compute max only for reference arm ---> for visual feedback
            if tag=='max_push':
                push_arr.append(sample[self.ref_inx])
            elif tag=='max_pull':
                pull_arr.append(sample[self.ref_inx])
        
        self.record_to_file(self.to_record_arr,self.savepath_cali)
        self.max_push,self.max_pull=get_maximum(push_arr,pull_arr)   
        print('max push:',self.max_push,'max_pull:',self.max_pull)
        

        self.game=gamer()

        time.sleep(5)
        self.to_record_arr=[]
        self.counter=0
        self.record_flag=False
        self.now=time.time()
        
        try:
            NI=ni_stream('game')
            NI.start_streaming(channels,self.callback_game,ni_fs)
        except: pass

        self.record_to_file(self.to_record_arr,self.savepath_game)
 
    
    def callback_cali(self,sample):
        if type(sample)!=list:
            sample=[sample]
             
        # print(sample)
        if self.counter>self.render_lag:
            self.record_flag,self.tag=self.pre_exp.logic(sample)
            self.counter=0

        if self.record_flag:
            timestamp=time.time()-self.now
            self.to_record_arr.append([sample,self.tag,timestamp])

        self.counter+=1
        ##Test sampling rate#####
        # self.counter+=1
        # timestamp=time.time()
        # elapsed=timestamp-self.now
        # if elapsed>2.0:
        #     fs=self.counter/2.0
        #     print(fs)
        #     self.counter=0
        #     self.now=time.time()
       

    def callback_game(self,sample):
        

        if type(sample)!=list:
            sample=[sample]
        raw_torque=[]
        for i in range(len(sample)):
            chn_data=sample[i]-self.offset[i]
            raw_torque.append(CALIBRATION[i]*chn_data)
        
        abs_torque=[abs(ele) for ele in raw_torque]
        if self.counter>self.render_lag:
            

            self.game.game_logic(abs_torque,abs(self.max_push*0.4),self.ref_inx)
            self.counter=0

        if self.record_flag:
            timestamp=time.time()-self.now
            self.to_record_arr.append([sample,self.tag,timestamp])

        self.counter+=1

    def record_to_file(self,array,savepath):
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
        with open(savepath,'a') as f:
            f.write(row)

######helper function###############

def get_maximum(push_arr,pull_arr):
    """return [push max, pull max]"""
    window_size=200
    step_size=1
    max_push=0
    max_pull=0
    push_p=0
    push_n=0

    print("record length:",len(push_arr),len(pull_arr))
    for ele in push_arr:
        if np.sign(ele)>0:
            push_p+=1
        else:
            push_n+=1
    
    if push_p>push_n:
        #push on reference arm ---> positivie signal
        #pull --> negative
        for i in range(len(push_arr)-window_size):
            c_win=push_arr[i:i+window_size]
            c_ma=np.average(c_win)
            
            if c_ma>=max_push:
                max_push=c_ma
   
    

        for i in range(len(pull_arr)-window_size):
            c_win=pull_arr[i:i+window_size]
            c_ma=np.average(c_win)
            if c_ma<=max_pull:
                max_pull=c_ma

        
        return [max_push,max_pull]
        
    elif push_p<push_n:
        #push on reference arm ---> negative signal
        #pull --> postivie
        for i in range(len(push_arr)-window_size):
            c_win=push_arr[i:i+window_size]
            c_ma=np.average(c_win)
            
            if c_ma<=max_push:
                max_push=c_ma
       
    
   
        for i in range(len(pull_arr)-window_size):
            c_win=pull_arr[i:i+window_size]
            c_ma=np.average(c_win)
            if c_ma>=max_pull:
                max_pull=c_ma
          
        
        return [max_push,max_pull]
    else:
        warnings.warn('Cannot figure out sign of the reference sensor.')


def main():
    signal_processor(ni_fs=800)    

if __name__ == '__main__':
	main()