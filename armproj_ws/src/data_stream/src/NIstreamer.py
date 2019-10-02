#!/usr/bin/env python3

import nidaqmx as daq
import time
import warnings
        
def start_streaming(channels,callback,ni_fs=1000): 
    """
    defines channels to read, write a callback function to do signal processing
    default frame rate =1k Hz

    channels: list of strings eg. ["Dev1/ai0","Dev1/ai1"]
    callback: can take multiple callback functions as list
    ni_fs: sample rate
    """
    period=1.0/ni_fs

    try:
        daqtask=daq.Task()
    except:
        raise ValueError('Unable to connect to DAQ device')     
    for chn in channels:
        daqtask.ai_channels.add_ai_voltage_chan(chn)
    
    while True:
        now=time.time()
        
        raw_sig=daqtask.read()
        callback(raw_sig)

        elapsed=time.time()-now
        try:
            time.sleep(period-elapsed)
        except:
            warnings.warn('System cannot handle such hight frame rate, lower the desired frequency or simplify your callback fucntion')
            continue


        
