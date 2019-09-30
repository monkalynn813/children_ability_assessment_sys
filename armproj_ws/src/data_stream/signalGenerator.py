'''
signalGenerator for torque testing programs
Intakes analog signal from niDAQ box, and posts values to a udp socket
Runs indefinitely

Last edited by Jackson Bremen 8/15/2019
'''

import socket
import nidaqmx as daq
import numpy

print("Attempting to connect to DAQ")

try:
    myTask = daq.Task() #Create a DAQ task
    myTask.ai_channels.add_ai_voltage_chan("Dev1/ai1") #Channel to read in on goes here
    # creates a channel connection through the task
except:
    print("Failed to connect to DAQ. Check connections and DAQ status.")
    print("Exiting safely")
    exit(0)

UDP_IP = "127.0.0.1" #Localhost IP to post values to 
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((UDP_IP, UDP_PORT)) #connect to the udp socket

print("Successfully onnected to socket, reading and sending data")

while True: #TODO find a way to safely shut down the tasks, rather than having to force terminate thread
    MESSAGE = myTask.read()

    sock.send(str(MESSAGE).encode())
    # Currently sends the message as a string, as it preserves decimal precision

print('done')
myTask.close()
