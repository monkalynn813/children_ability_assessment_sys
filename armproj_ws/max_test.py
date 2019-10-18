#!/usr/bin/env python

import pygame
import numpy as np
import random
import time
import socket
import json

path='/home/jingyan/Documents/spring_proj/armproj_ws/img/'
# path='C:\\Users\\pthms\\Desktop\\ling\\children_ability_assessment_sys\\armproj_ws\\src\\arm_game\\src\img\\'

UDP_IP = "127.0.0.1" 
FLAG_PORT=5004

class calibrator(object):
    def __init__(self):
        self.sock_flag = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)