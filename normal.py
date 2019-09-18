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
import time
import cv2 as cv
import numpy as np
import random
from PIL import Image

# relative module
import video

# built-in module
import sys
cv.setUseOptimized(True)
car_cascade = cv.CascadeClassifier('cascade_11xx_11xx_LBP_24_24_anno.xml')

if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass
    cv.namedWindow('video')
    print(fn)
    cap = video.create_capture(fn)
    #get fps
    fps = cap.get(cv.CAP_PROP_FPS)
    print('Video\'s FPS: {:f}'.format(fps))
    #processing
    cnt=0
    Velocity=40
    Acceleration=random.uniform(-2.0,2.0)
    BreakForce=0
    f=0
    kernel = np.ones((5,5),np.uint8)
    t1=time.time()
    while True:
        p1=time.time()

        Velocity += Acceleration
        Acceleration=random.uniform(-2.0,2.0)

        flag, img = cap.read()

        #lowerize the quality to make the pFPS higher
        h,w,depth=img.shape
        img=cv.resize(img,(int(w/2),int(h/2)),interpolation=cv.INTER_AREA)
        
        #height, width = img.shape[:2]
        #print(height,width)
        #cut test.mp4
        #img = img[80:,:]
        #cut 20190304....
        #img = img[540:1080,:]

        #test
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        #gray = cv.GaussianBlur(gray,(3,3),0)
        gray=cv.bilateralFilter(gray, 5, 21, 21)
        #gray = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel)
        
        
        '''
        thrs1 = cv.getTrackbarPos('thrs1', 'edge')
        thrs2 = cv.getTrackbarPos('thrs2', 'edge')
        #edge
        edge = cv.Canny(gray, thrs1, thrs2, apertureSize=5)
        
        vis = img.copy()
        vis = np.uint8(vis/2.)
        vis[edge != 0] = (0, 255, 0)
        cv.imshow('edge', vis)
        '''

        cars=car_cascade.detectMultiScale(gray, 1.1, 1)
        for (x,y,w,h) in cars:
            cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv.putText(img , 'Velocity:%f'%(Velocity) , (10,10) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
        cv.putText(img , 'FPS:%f'%(f) , (10,30) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
        cv.imshow('video', img)
        
        
        ch = cv.waitKey(5)
        cnt=cnt+1
        p2=time.time()
        f=1/(p2-p1)
        if ch == 27:
            break
    t2=time.time()
    print('Process time: {:f}'.format(t2-t1))
    print('Frame count: {:d}'.format(cnt))
    print('pFPS: {:f}'.format(1/((t2-t1)/cnt)))
    cv.destroyAllWindows()
