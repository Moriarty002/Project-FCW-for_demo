#!/usr/bin/env python
# Python 2/3 compatibility
from __future__ import print_function
import queue
import os
import random
import threading
import time
import cv2 as cv
import numpy as np
from PIL import Image
#import RPi.GPIO as GPIO
# relative module
import video
# built-in module
import sys
# garbage collection
import gc

import Distance_function

cv.setUseOptimized(True)
car_cascade = cv.CascadeClassifier('cascade_10000_30000.xml')

if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    cv.namedWindow('video')
    #get video
    cap = video.create_capture(fn)
    #get fps
    fps = cap.get(cv.CAP_PROP_FPS)
    #set how many threads could be run in same time
    #count frame
    cnt=0
    '''
    #GPIO set
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    '''
    #other variables
    Velocity=60
    Acceleration=np.linspace(920,20,10)
    BreakForce=0
    IpFPS=0
    Q=queue.Queue(maxsize=30)
    #processing
    #record the start time
    t1=time.time()
    while True:
        p1=time.time()
        flag, img = cap.read()

        #lowerize the quality to make the pFPS higher
        h,w,depth=img.shape
        img=cv.resize(img,(int(w/2),int(h/2)),interpolation=cv.INTER_AREA)
        
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img2=img
        ace=random.random()
        if(Velocity>80):
            Velocity -= ace
        elif(Velocity<40):
            Velocity += ace
        else:
            if(random.randint(1,10)%2==0):
                Velocity+=ace
            else:
                Velocity-=ace
        gray=cv.bilateralFilter(gray, 5, 21, 21)
        d=[]
        S=0
        cars = car_cascade.detectMultiScale(gray, 1.5, 4)
        Cac=cars
        v=Velocity
        v2=v
        if(len(Cac)> 0):
            b=Cac[:,2:3]
            b=[float(tmp) for tmp in b]
            b=[63360/tmp for tmp in b]
            v=v*27.78
            c=[(v*v)/tmp for tmp in Acceleration]
            for i in b :
                for j in range(0,11) :
                    if(i < c[j]):
                        d.append(j)
                        break
            d=[10-tmp for tmp in d]
        d=[tmp for tmp in d]
        if(len(d)>3):
            e=d.sort(reverse=True)
            e=d[0:3]
        elif(len(d))>0:
            e=d
        else:
            e=[0,0]
        
        for i in e:
            if(Q.full()):
                Q.get()
            Q.put(i)
    
        if(not Q.empty()):
            L=list(Q.queue)
            S=sum(L)
            S/=Q.qsize()
            #LEDcontrolBreak(S)
        
        for (x,y,w,h) in cars:
            cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    
        cv.putText(img , 'Velocity:%f'%(v2) , (10,10) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
        p2=time.time()
        IpFPS=1/(p2-p1)
        cv.putText(img , 'FPS:%f'%(IpFPS) , (10,30) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
        cv.putText(img , 'Num:%d'%(S) , (10,50) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
        cv.imshow('video', img)
        
        ch = cv.waitKey(5)
        cnt=cnt+1
        if ch == 27:
            break
    t2=time.time()
    print('Process time: {:f}'.format(t2-t1))
    print('Frame count: {:d}'.format(cnt))
    print('pFPS: {:f}'.format(1/((t2-t1)/cnt)))
    cv.destroyAllWindows()