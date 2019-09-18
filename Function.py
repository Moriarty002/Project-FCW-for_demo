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
'''
SMALL=LED(18)
BIG=LED(12)
SMOG=LED(32)
'''
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
    if(Cac.size > 0):
        b=Cac[:,2:3].copy()
        b=b.astype(float)
        b=63360/b
        v=v*27.78
        c=(v*v)/Acceleration
        d=np.searchsorted(c,b)
        d=10-d
    d=np.append(d,[0,0,0])
    d=d.flatten()
    e=d[np.argpartition(d, -3)[-3:]]
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
    
    cv.putText(img , 'Velocity:%f'%(60) , (10,10) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    p2=time.time()
    IpFPS=1/(p2-p1)
    cv.putText(img , 'FPS:%f'%(IpFPS) , (10,30) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    cv.putText(img , 'Num:%d'%(S) , (10,50) ,cv.FONT_HERSHEY_TRIPLEX,0.5,(0, 0, 255),1,4)
    cv.imshow('video', img)
    lock.release()
def Brightness(flag,img,img2,lock):
	lock.acquire()
	cimg=img[0:80,100:220]
	hls = cv.cvtColor(cimg, cv.COLOR_BGR2HLS_FULL)
	L=np.array(hls[:,:,1])
	L=L.flatten()
	L/=16
	m=np.bincount(L)
	M=np.argmax(m)
	print(M)
	var = SMOGdetect(img2)
	print(var)
	lock.release()
def SMOGdetect(img):
	vars=[]
	for x in img :
		variance=np.var(x)
		vars.append(variance)
	return np.mean(vars)    

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
def LEDcontrolLight(s):
    if(s<5):
        SMALL.on()
        SMOG.off()
        BIG.off()
    elif(s<8):
        BIG.on()
        SMALL.off()
        SMOG.off()
    else:
        SMOG.on()
        SMALL.off()
        BIG.off()
    return
'''