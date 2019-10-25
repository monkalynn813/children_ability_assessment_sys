#!/usr/bin/env python

import pygame
import numpy as np
import random
import time


path='/home/jingyan/Documents/spring_proj/armproj_ws/img/'
# path='C:\\Users\\pthms\\Desktop\\ling\\children_ability_assessment_sys\\armproj_ws\\src\\arm_game\\src\img\\'


class calibrator(object):
    def __init__(self):
        pygame.init()
        self.screenwidth=1290
        self.screenheight=768
        self.win=pygame.display.set_mode((self.screenwidth,self.screenheight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Assessment Calibration")

        ##init##
        self.showpic_init()
        self.zero_init()

        self.run=True
        self.logic([1,4])
    def showpic_init(self):
        self.bgpic=showpic_generator()
    def zero_init(self):
        self.zero_flag=False
        self.zero_done_flag=False
        self.data_4cali=[]
        self.offset=[]
    def logic(self,signal):
        while self.run:
            self.clock.tick(27)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            keys=pygame.key.get_pressed()

            if keys[pygame.K_RETURN]:
                #get average in 3s and set as offset
                self.zero_flag=True
                now=time.time()
            
            if self.zero_flag:
                print('geting the offset')
                self.data_4cali.append(signal)
                eclapsed= time.time()-now
                if eclapsed>3.0:
                    self.zero_flag=False
                    data4cali=np.array(self.data_4cali)
                    for i in range(len(data4cali[0])):
                        offset_=np.average(data4cali[:,i])
                        self.offset.append(offset_)
                    self.zero_done_flag=True
            
            if self.zero_done_flag and keys[pygame.K_BACKSPACE]:
                self.zero_done_flag=False
                self.data_4cali=[]
                self.offset=[]
                self.zero_flag=True
                now=time.time()
           
            
            self.draw()

    def draw(self):
        self.win.blit(self.bgpic.bg,(0,0))

        if self.zero_done_flag:
            font=pygame.font.SysFont("comicsansms",75)
            self.zero_result=font.render(str(self.offset), True, (43, 9, 183))
            self.win.blit(self.zero_result,(self.screenwidth//2-self.zero_result.get_width()//2,self.screenheight//2-self.zero_result.get_height()//2))



        pygame.display.update()


class showpic_generator(object):
    def __init__(self):
        
        global path
        self.bg=pygame.image.load(path+'bg2.jpg')
        self.bg=pygame.transform.scale(self.bg,(1290,768))

def main():
    calibrator()    
            
if __name__ == '__main__':
	main()