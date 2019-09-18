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

import Ligth_function

cv.setUseOptimized(True)
RUN_SIG = True
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
    semaphore = threading.Semaphore(2)
    #count frame
    cnt=0
    global RUN_SIG
    t1=time.time()
    while (RUN_SIG):
        cnt =cnt+1
        flag, img = cap.read()
        h,w,depth=img.shape
        w/=2
        h/=2
        img=cv.resize(img,(int(w),int(h)),interpolation=cv.INTER_AREA)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #less the threads in pool to prevent overusing the memory
        #and make sure that the processing frame is the newest
        if threading.activeCount()>5:
            continue
        fh=threading.Thread(target = Ligth_function.Brightness, args = (flag,img,gray,semaphore))
        fh.setDaemon(True)
        fh.start()
        #collect the garbage in memory
        gc.collect()
        #if "esc" key was pressed , break and leave
        
    t2=time.time()
    #GPIO.cleanup()
    print('Video\'s FPS: {:f}'.format(fps))
    print('Process time: {:f}'.format(t2-t1))
    print('Frame count: {:d}'.format(cnt))
    print('pFPS: {:f}'.format(1/((t2-t1)/cnt)))