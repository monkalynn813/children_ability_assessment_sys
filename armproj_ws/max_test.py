#!/usr/bin/env python

import pygame
import numpy as np
import random
import time


path='/home/jingyan/Documents/spring_proj/armproj_ws/img/'
# path='C:\\Users\\pthms\\Desktop\\ling\\children_ability_assessment_sys\\armproj_ws\\img\\'


class calibrator(object):
    def __init__(self,savepath=None):
        self.savepath=savepath

        pygame.init()
        self.screenwidth=1290
        self.screenheight=768
        self.win=pygame.display.set_mode((self.screenwidth,self.screenheight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Assessment Calibration")

        ##init##
        self.showpic_init()
        self.zero_init()
        self.test_hint_init()
        self.progressbar_init()

        

        self.run=True
        while self.run:
            self.logic([1,4])
    def record_to_file(self,data,tag):
        """
        type(data)==list
        [sensor_data,sensor_data,...]
        tag=str i.e 'reference'
        """
        row=''
        for d in data:
            row+=str(d)
            row+=','
        row+=str(tag)
        row+='\n'
        with open(self.savepath,'a') as f:
            f.write(row)
    def showpic_init(self):
        self.bgpic=showpic_generator()
    def zero_init(self):
        self.zero_flag=False
        self.zero_done_flag=False
        self.data_4cali=[]
        self.offset=[]
    def test_hint_init(self):
        self.max_torque_test=False
        self.max_push_hint=False
        self.max_pull_hint=False
        self.do_push_test=False
        self.do_pull_test=False
        self.push_test_done=False
        self.pull_test_done=False
    def progressbar_init(self):
        self.cali_progress=progressbar_generator(self.screenwidth//2-100,self.screenheight//2 +50,0,40,(65, 220, 244))  
        self.test_progress=progressbar_generator(self.screenwidth//2,self.screenheight//2,0,40,(65,220,244))
    def logic(self,signal):
        # while self.run:
        self.clock.tick(27)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        keys=pygame.key.get_pressed()

        #Do the zeroing
        if not self.zero_done_flag and keys[pygame.K_RETURN]:
            #get average in 3s and set as offset
            self.zero_flag=True
            self.now=time.time()
        
        if self.zero_flag:
            self.data_4cali.append(signal)
            eclapsed= time.time()-self.now
            self.cali_progress.width += 2
            self.cali_percent=round(eclapsed / 3, 3) * 100
            if eclapsed>3.0:
                self.zero_flag=False
                data4cali=np.array(self.data_4cali)
                for i in range(len(data4cali[0])):
                    offset_=np.average(data4cali[:,i])
                    self.offset.append(offset_)
                self.zero_done_flag=True
        
        #Redo the zeroing
        if self.zero_done_flag and not self.max_torque_test and keys[pygame.K_BACKSPACE]:
            self.zero_done_flag=False
            self.data_4cali=[]
            self.offset=[]
            self.zero_flag=True
            self.cali_progress.width = 0
            self.now=time.time()
        
        #Press Enter at offset screen to start maximum torque test
        if self.zero_done_flag and not self.max_torque_test and keys[pygame.K_RETURN]:
            self.max_torque_test=True
            self.max_push_hint=True
            
        
        if self.max_push_hint and keys[pygame.K_SPACE]:
            self.max_push_hint=False
            self.do_push_test=True #replace this for actual visual feedback later
            self.now=time.time()

        if self.do_push_test:
            
            if keys[pygame.K_RIGHT]:
                self.test_progress.width += 3
            elif self.test_progress.width>0: 
                self.test_progress.width -= 6
            eclapsed=time.time()-self.now
            self.time_left= int(5- eclapsed)
            if eclapsed > 5.0:
                self.do_push_test=False
                self.push_test_done=True

        if self.push_test_done and not self.do_pull_test:
            self.test_progress.width=0
            if keys[pygame.K_BACKSPACE]:
                self.push_test_done=False
                self.max_push_hint=True
            if keys[pygame.K_RETURN]:
                self.max_pull_hint=True
        
        if self.max_pull_hint and keys[pygame.K_SPACE]:
            self.max_pull_hint=False
            self.do_pull_test=True
            self.now=time.time()
        
        if self.do_pull_test:
            if keys[pygame.K_LEFT]:
                self.test_progress.width -= 3
            elif self.test_progress.width <0: 
                self.test_progress.width += 6
            eclapsed=time.time()-self.now
            self.time_left= int(5- eclapsed)
            if eclapsed > 5.0:
                self.do_pull_test=False
                self.pull_test_done=True
        
        if self.pull_test_done:
            self.test_progress.width=0
            if keys[pygame.K_BACKSPACE]:
                self.pull_test_done=False
                self.max_pull_hint=True
            if keys[pygame.K_RETURN]:
                pygame.quit()



        self.draw()

    def draw(self):
        self.win.blit(self.bgpic.bg,(0,0))
        
        if self.zero_flag:
            font=pygame.font.SysFont("comicsansms",75)
            self.hint=font.render("Calibrating ... " + str(self.cali_percent) + '%'  , True, (43, 9, 183))
            self.win.blit(self.hint,(self.screenwidth//2-self.hint.get_width()//2,self.screenheight//2-self.hint.get_height()//2))
            pygame.draw.rect(self.win,self.cali_progress.color, (self.cali_progress.x,self.cali_progress.y,self.cali_progress.width,self.cali_progress.height))
        #show offset after zeroing
        if self.zero_done_flag and not self.max_torque_test:
            font=pygame.font.SysFont("comicsansms",25)
            self.zero_result=font.render(str(self.offset), True, (43, 9, 183))
            self.win.blit(self.zero_result,(self.screenwidth//2-self.zero_result.get_width()//2,self.screenheight//2-self.zero_result.get_height()//2))
        if self.max_push_hint:
            font=pygame.font.SysFont("comicsansms",75)
            self.hint=font.render("Push the best you can for 5 sec", True, (43, 9, 183))
            self.win.blit(self.hint,(self.screenwidth//2-self.hint.get_width()//2,self.screenheight//2-self.hint.get_height()//2))
        if self.max_pull_hint:
            font=pygame.font.SysFont("comicsansms",75)
            self.hint=font.render("Pull the best you can for 5 sec", True, (43, 9, 183))
            self.win.blit(self.hint,(self.screenwidth//2-self.hint.get_width()//2,self.screenheight//2-self.hint.get_height()//2))
        if self.do_push_test or self.do_pull_test:
            font=pygame.font.SysFont("comicsansms",90)
            self.hint=font.render(str(self.time_left), True, (43, 9, 183))
            self.win.blit(self.hint,(self.screenwidth//2-self.hint.get_width()//2,self.screenheight//2-2*self.hint.get_height()))
            pygame.draw.rect(self.win,self.test_progress.color, (self.test_progress.x,self.test_progress.y,self.test_progress.width,self.test_progress.height))
        
        
        
        pygame.display.update()

class progressbar_generator(object):
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.color=color

class showpic_generator(object):
    def __init__(self):
        
        global path
        self.bg=pygame.image.load(path+'bg2.jpg')
        self.bg=pygame.transform.scale(self.bg,(1290,768))

def main():
    calibrator()    
            
if __name__ == '__main__':
	main()