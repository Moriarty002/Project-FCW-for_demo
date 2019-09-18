#!/usr/bin/env python

'''
This sample demonstrates Canny edge detection.

Usage:
  edge.py [<video source>]

  Trackbars control edge thresholds.

'''

# Python 2/3 compatibility
from __future__ import print_function

import os
import random
import thread
import time
import cv2 as cv
import numpy as np
from PIL import Image

# relative module
import video

# built-in module
import sys

# garbage collection
import gc

cnt=0
car_cascade = cv.CascadeClassifier('cascade_11xx_11xx_LBP_24_24_anno.xml')
thread.LockType='spinLock'


def VideoTest(flag,img,lock,v):
    lock.acquire()
    #height, width = img.shape[:2]
    
    #cut test.mp4
    #img = img[80:,:]
    #cut 20190304....
    #img = img[540:1080,:]

    #lowerize the quality to make the pFPS higher
    h,w,depth=img.shape
    img=cv.resize(img,(int(w/3),int(h/3)),interpolation=cv.INTER_AREA)

    #test
        
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray,(3,3),0)
    #thrs1 = cv.getTrackbarPos('thrs1', 'edge')
    #thrs2 = cv.getTrackbarPos('thrs2', 'edge')
    '''
    #edge
    #edge = cv.Canny(gray, thrs1, thrs2, apertureSize=5)   
    vis = img.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)
    cv.imshow('video', vis)
    '''
    cars=car_cascade.detectMultiScale(gray, 1.1, 1)
    for (x,y,w,h) in cars:
        cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    cv.putText(img , 'Velocity:%f'%(v) , (10,180) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    cv.imshow('video', img)
    
    global cnt
    cnt=cnt+1
    lock.release()
    thread.exit()
    
if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    cv.namedWindow('video')
    #cv.createTrackbar('thrs1', 'edge', 2000, 5000, nothing)
    #cv.createTrackbar('thrs2', 'edge', 4000, 5000, nothing)

    cap = video.create_capture(fn)
    #get fps
    fps = cap.get(cv.CAP_PROP_FPS)
    print(thread.LockType)
    print('Video\'s FPS: {:f}'.format(fps))
    #processing
    #using lock preventing from race condition
    lock = thread.allocate_lock()
    global cnt
    t1=time.time()
    Velocity=40
    Acceleration=random.uniform(-2.0,2.0)
    BreakForce=0
    while True:

        flag, img = cap.read()
        Velocity+=Acceleration
        Acceleration=random.uniform(-2.0,2.0)
        thread.start_new_thread( VideoTest, (flag,img,lock,Velocity))
        gc.collect()
    
        #VideoTest(flag,img)
        
        ch = cv.waitKey(5)
        if ch == 27:
            break
    t2=time.time()
    print('Process time: {:f}'.format(t2-t1))
    print('Frame count: {:d}'.format(cnt))
    print('pFPS: {:f}'.format(1/((t2-t1)/cnt)))
    cv.destroyAllWindows()
