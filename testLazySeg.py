'''
Created on Feb 6, 2014

@author: Valerie
'''
import io
import time
#import picamera
#from imgProc import imgProc
#from PIL import Image
from skimage import io as skio
from skimage import color
import numpy as np
import cv2
import matplotlib.pyplot as plt
#import threading
#from easyEBB import easyEBB
def tic():
    return time.time()
def toc(t):
    return time.time() - t
    

DURATION = 1000; #in ms
STEPX = 1/100 #pixels per step
STEPY = 1/100 #pixels per step
BOUNDX = 200; #pixels
BOUNDY = 200; #pixels
VIDLEN = 120; #in sec
PING = 0.5; #in sec
WINDOW = 10; #number of frames to average
i = 0

cap = cv2.VideoCapture('C:\\Users\\Valerie\\Desktop\\spyspace\\nem\\led_move1.avi')
#ret, frame = cap.read()

startT = time.time() # start time
lastCheck = startT - PING # artificial last check
now = startT
ref = None;
print "size ref: %d" % np.size(ref)
xds = [];
yds = [];
xr = 0;
yr = 0;
try: 
    #while cap.isOpened():
    while now - startT <= VIDLEN: #while less than video length
        now = time.time()
        #camera.wait_recording(1)
        if now - lastCheck >= PING:
            ret, frame = cap.read()
            t = tic()
            lastCheck = time.time()
            #camera.capture(stream2, format='jpeg', use_video_port = True)
            #stream2.seek(0)
            img = color.rgb2gray(frame)
            if np.size(ref) == 1:
                ref = img;
                xr, yr = np.nonzero(ref == np.min(ref))
                print "xr:\t%d\tyr:\t%d" % (xr[0], yr[0])
            else: 
                sub = img - ref
                x, y = np.nonzero(sub == np.max(sub))
                print "x:\t%d\ty:\t%d" % (x[0], y[0])
                xds.append(x[0] - xr[0])
                yds.append(y[0] - yr[0])
                #plt.imshow(sub, cmap = 'gray')
                ##plt.scatter(x[0], y[0])
                #plt.scatter(xr[0], yr[0])
                #plt.show()
                #print xds
                #print yds
                #print "len: %d" % len(xds)
                if (len(xds) > WINDOW):
                    xds.pop(0)
                    yds.pop(0)
                mx = np.mean(xds)
                my = np.mean(yds)
                #print "mean x: %d y: %d" % (mx, my)    
               
                if abs(mx) > BOUNDX or abs(my) > BOUNDY:
                    #print "move: %d, %d" % (mx, my)
                    plt.imshow(sub, cmap = 'gray')
                    plt.scatter(x[0], y[0])
                    plt.scatter(xr[0], yr[0])
                    plt.show()
                    ref = None
                print "time: %f s" % toc(t)
                i = i+1
                print i
finally:
    print 'done finally'
print 'done'