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
import signal
#import RPi.GPIO as GPIO
# relative module
import video
# built-in module
import sys
# garbage collection
import gc

import Extra_function

cv.setUseOptimized(True)
RUN_SIG = True
car_cascade = cv.CascadeClassifier('cascade_10000_30000.xml')

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    global RUN_SIG 
    RUN_SIG = False

if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    
    signal.signal(signal.SIGINT, signal_handler)
    #get video
    cap = video.create_capture(fn)
    #get fps
    fps = cap.get(cv.CAP_PROP_FPS)
    #set how many threads could be run in same time
    semaphore = threading.Semaphore(4)
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
    global RUN_SIG
    t1=time.time()
    while (RUN_SIG):
        #get frame from input video and compress it
        flag, img = cap.read()
        h,w,depth=img.shape
        w/=2
        h/=2
        img=cv.resize(img,(int(w),int(h)),interpolation=cv.INTER_AREA)
        img2=img
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ace=random.random()
        #less the threads in pool to prevent overusing the memory
        #and make sure that the processing frame is the newest
        if threading.activeCount()>4:
            continue
        cnt =cnt+1
        #put frame and other message into thread and run it 
        if(Velocity>80):
            Velocity -= ace
        elif(Velocity<40):
            Velocity += ace
        else:
            if(random.randint(1,10)%2==0):
                Velocity+=ace
            else:
                Velocity-=ace
        th=threading.Thread(target = Extra_function.Distance, args = (flag,gray,img,semaphore,Velocity,Q,Acceleration,car_cascade))
        th.setDaemon(True)
        th.start()
        gc.collect()
    t2=time.time()
    #GPIO.cleanup()
    print('Video\'s FPS: {:f}'.format(fps))
    print('Process time: {:f}'.format(t2-t1))
    print('Frame count: {:d}'.format(cnt))
    print('pFPS: {:f}'.format(1/((t2-t1)/cnt)))