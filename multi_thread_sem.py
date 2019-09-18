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

# relative module
import video

# built-in module
import sys

# garbage collection
import gc

cv.setUseOptimized(True)
car_cascade = cv.CascadeClassifier('cascade_10000_30000.xml')

def VideoTest(flag,img,lock,v,Q,Acceleration):
    p1=time.time()
    lock.acquire()
    d=np.array(0)
    S=0
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray=cv.bilateralFilter(gray, 5, 21, 21)
    #gray = cv.GaussianBlur(gray,(3,3),0)
    #gray = cv.morphologyEx(gray, cv.MORPH_GRADIENT, kernel)
    
    cars=car_cascade.detectMultiScale(gray, 1.5, 4)
    Cac=np.array(cars)
    if(Cac.size > 0):
        a=Cac[:,1:2].copy()
        b=Cac[:,2:3].copy()
        a=240-(a+b)
        b=b.astype(float)
        b=63360/b
        v=v*27.78
        c=(v*v)/Acceleration
        #a:y,b:DistanceToCar(cm),c:DistanceFromSafe
        d=np.searchsorted(c,b)
        d=10-d
    d=np.append(d,[0,0,0])
    d=d.flatten()
    e=d[np.argpartition(d, -3)[-3:]]
    for i in e:
        if(Q.full()):
            Q.get()
        Q.put(i)
    
    if(not Q.empty()):
        L=list(Q.queue)
        S=sum(L)
        S/=Q.qsize()
      
    for (x,y,w,h) in cars:
        cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    
    cv.putText(img , 'Velocity:%f'%(v) , (10,10) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    p2=time.time()
    IpFPS=1/(p2-p1)
    cv.putText(img , 'FPS:%f'%(IpFPS) , (10,30) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    cv.putText(img , 'Num:%d'%(S) , (10,50) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    cv.imshow('video', img)
    lock.release()

    
if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    cv.namedWindow('video')

    cap = video.create_capture(fn)
    #get fps
    fps = cap.get(cv.CAP_PROP_FPS)
    semaphore = threading.Semaphore(2)
    cnt=0
    t1=time.time()
    
    Velocity=40
    Acceleration=np.linspace(920,20,10)
    BreakForce=0
    IpFPS=0
    Q=queue.Queue(maxsize=30)
    while True:
        cnt =cnt+1
        flag, img = cap.read()
        #print(threading.activeCount())
        #print('\n')

        #lowerize the quality to make the pFPS higher
        h,w,depth=img.shape
        w/=2
        h/=2
        img=cv.resize(img,(int(w),int(h)),interpolation=cv.INTER_AREA)
        #print(w,h)
        #print('there are ', threading.activeCount(), 'threads running')
        if threading.activeCount()>5:
            cv.imshow('video', img)
            continue
        #Velocity+=Acceleration
        #Acceleration=random.uniform(-2.0,2.0)
        th=threading.Thread(target = VideoTest, args = (flag,img,semaphore,Velocity,Q,Acceleration))
        th.setDaemon(True)
        th.start()
        
        gc.collect()
        #VideoTest(flag,img)
        
        ch = cv.waitKey(5)
        if ch == 27:
            break
    t2=time.time()    
    print('Video\'s FPS: {:f}'.format(fps))
    print('Process time: {:f}'.format(t2-t1))
    print('Frame count: {:d}'.format(cnt))
    print('pFPS: {:f}'.format(1/((t2-t1)/cnt)))

    cv.destroyAllWindows()
