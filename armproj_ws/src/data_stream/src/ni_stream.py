#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32

class streamer(object):
    def __init__(self):



        #####publisher#####
        self.raw_publisher=rospy.Publisher('/arm_interface/raw_data',Float32,queue_size=10)


def main():
    rospy.init_node("/arm_interface/data_streamer",anonymous=True)
    rospy.loginfo("===Streaming data====")

    
    try:
        streamer()    
        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()