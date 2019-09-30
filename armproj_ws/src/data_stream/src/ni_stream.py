#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
import numpy as np 
import nidaqmx as daq

class streamer(object):
    def __init__(self,channels=["Dev1/ai1"]):
        self.channels=channels

        self.raw_sig_arr=[]
        #####publisher#####
        self.raw_publisher=rospy.Publisher('/arm_interface/raw_data',Float32,queue_size=10)
        self.filtered_publisher=rospy.Publisher('/arm_interface/filtered_data',Float32,queue_size=10)
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

        self.filter_bp(raw_sig)

    def filter_bp(self,sample):
        self.raw_sig_arr.append(sample)



def main():
    rospy.init_node("data_streamer",anonymous=True)
    rospy.loginfo("===Streaming data====")

    
    try:
        streamer()    
        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()