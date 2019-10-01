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
    d=np.array(0)
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
    Cac=np.array(cars)
    v2=v
    if(Cac.size > 0):
        b=Cac[:,2:3].copy()
        b=b.astype(float)
        b=63360/b
        v=v*27.78
        c=(v*v)/Acceleration
        d=np.searchsorted(c,b)
        d=10-d
    d=d.flatten()
    if(len(d)>3):
        e=d[np.argpartition(d, -3)[-3:]]
    elif(len(d))>0:
        e=d
    else:
        e=np.array([0,0]).flatten()
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