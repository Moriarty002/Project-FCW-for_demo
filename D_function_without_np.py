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
RED=32
BLUE=12
GREEN=18

def Distance(flag,gray,img,lock,v,Q,Acceleration,car_cascade):
    #variables declare
    p1=time.time()
    lock.acquire()
    d=[]
    S=0
    #make blur
    gray=cv.bilateralFilter(gray, 5, 21, 21)
    #car detect
    cars=car_cascade.detectMultiScale(gray, 1.5, 4)
    #vectorize "cars"
    '''
    b:the distance between camera and detected cars(unit:cm)
    c:the safe distance with different break force(from 10(cm/s*s) to 460(cm/s*s))
    d:find out which region sould detected cars located
    e:the top 3 of d
    '''
    Cac=cars
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
    '''
    operate Queue to communicate with other threads
    and record the result of self
    '''
    for i in e:
        if(Q.full()):
            Q.get()
        Q.put(i)
    
    if(not Q.empty()):
        L=list(Q.queue)
        S=sum(L)
        S/=Q.qsize()
        #LEDcontrolBreak(S)
    '''
    output frame with various messages
    Velocity : the emulated velocity of our car
    FPS      : the number to show the real time FPS
    Num      : the number to show the result
    '''
    for (x,y,w,h) in cars:
        cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    
    cv.putText(img , 'Velocity:%f'%(v2) , (10,10) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    p2=time.time()
    IpFPS=1/(p2-p1)
    cv.putText(img , 'FPS:%f'%(IpFPS) , (10,30) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    cv.putText(img , 'Num:%d'%(S) , (10,50) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    cv.imshow('video', img)
    lock.release()

'''
def LEDcontrolBreak(s):
    if(s<5):
        GPIO.output(GREEN,GPIO.HIGH)
        GPIO.output(RED,GPIO.LOW)
        GPIO.output(BLUE,GPIO.LOW)
    elif(s<8):
        GPIO.output(BLUE,GPIO.HIGH)
        GPIO.output(RED,GPIO.LOW)
        GPIO.output(GREEN,GPIO.LOW)
    else:
        GPIO.output(RED,GPIO.HIGH)
        GPIO.output(GREEN,GPIO.LOW)
        GPIO.output(BLUE,GPIO.LOW)
    return
'''