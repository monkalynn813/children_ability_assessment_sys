#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
import numpy as np 
import nidaqmx as daq
from scipy import signal

class streamer(object):
    def __init__(self,channels=["Dev1/ai1"],ni_fs=250):
        self.channels=channels
        self.ni_fs=ni_fs
        ######for filter#####
        self.raw_sig_arr=[]
        self.window_size=250
        self.cutoff_fq=2 #Hz
        #####publisher#####
        self.raw_publisher=rospy.Publisher('/arm_interface/raw_data',Float32,queue_size=10)
        self.filtered_publisher=rospy.Publisher('/arm_interface/filtered_data',String,queue_size=10)
        ###################

        try:
            self.daqtask=daq.Task()
            self.read_daq()
        except:
            rospy.logerr("Fail to connect to DAQ.")

        
    def read_daq(self):
        for chn in self.channels:
            self.daqtask.add_ai_voltage_chan(chn)
        
        raw_sig=self.daqtask.read()
        self.raw_publisher.publish(raw_sig)

        self.filter_lp(raw_sig)

    def filter_lp(self,sample):
        if len(self.raw_sig_arr)>=self.window_size and len(self.raw_sig_arr) %1==0:
            self.raw_sig_arr=self.raw_sig_arr[-self.window_size:]

            raw_sig_matrix=np.array(self.raw_sig_arr)
            filtered_data_allchn=[]
            for k in range(len(self.channels)):
                channel_raw=raw_sig_matrix[:,k]
                channel_filtered=lowpass(self.cutoff_fq,channel_raw,self.ni_fs)
                filtered_data_allchn.append(channel_filtered)
            
            self.filtered_publisher.publish(filtered_data_allchn)
        self.raw_sig_arr.append(sample)

def lowpass(cutoff,data,fs,order=5):
    nyq=0.5*fs
    normal_cutoff=cutoff/nyq
    b, a = signal.butter(order, normal_cutoff, btype='low',analog=False)
    return signal.lfilter(b, a, data, axis=0)

def main():
    rospy.init_node("data_streamer",anonymous=True)
    rospy.loginfo("===Streaming data====")

    
    try:
        streamer()    
        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()