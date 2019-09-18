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
SMALL=18
BIG=12
SMOG=32
def Brightness(flag,img,img2,lock):
    lock.acquire()
    cimg=img[0:80,100:220]    
    '''hls = cv.cvtColor(cimg, cv.COLOR_BGR2HLS_FULL)
    L=np.array(hls[:,:,1])
    L=L.flatten()
    L/=16
    m=np.bincount(L)
    M=np.argmax(m)'''
    M=np.mean(cimg)
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