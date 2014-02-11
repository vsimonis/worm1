'''
Created on Feb 11, 2014

@author: VSIMONIS
'''

import io
import camera
import numpy as np
from PIL import Image
import time
from easyEBB import easyEBB


#### Method definitions
def rgb2grayV(I):
    I = I.astype(float)
    try:
        np.size(I,2)
        J = 1.0/3 * (I[:,:,0]+ I[:,:,1] + I[:,:,2]);
        J = J.astype(int)
        return J
    except ValueError:
        print "Not a 3-D array"
        return
    

def findWorm(camera):
    global ref
    global xr, yr
    global xds, yds
    global WINDOW, BOUNDX, BOUNDY
    
    stream = io.BytesIO()
    camera.capture(stream, format ='jpeg', use_video_port = True)
    stream.seek(0)
    if ref is None:
        if V: print 'new reference'
        ref = rgb2grayV(Image.open(stream)).astype(float)
    else:
        if V: print 'new current'
        current = rgb2grayV(Image.open(stream)).astype(float)
        sub  = current - ref
        if V: print 'get max'
        x, y = np.nonzero(sub == sub.max())
        if xr is None: # Only get refernce coordinates if the reference is new
            if V: print 'get min'
            xr, yr = np.nonzero(sub == sub.min())
        # add distances to decision vector for average distance from ref
        if V: print 'append dists'
        xds.append(x[0] - xr[0])
        yds.append(y[0] - yr[0])
        
        if len(xds) > WINDOW:
            if V: print 'pop dists'
            xds.pop()
            yds.pop()
        
        if V: print 'mean dists'
        mx = np.mean(xds)
        yx = np.mean(yds)
        
        if abs(mx) > BOUNDX or abs(yx) > BOUNDY:
            print 'move'
            ref = None #will force a new reference image
            xr = None #will force a new reference coordinate
        
        return True

def write_vid(stream):
    with stream.lock:
        with io.open('dpu-test1.h264', 'wb') as out:
            for frame in stream.frames:
                if frame.header:
                    stream.seek(frame.position)
                    break
            while True:
                buf = stream.read1()
                if not buf:
                    break
                out.write(buf)
        stream.seek(0)
        stream.truncate()
    if V: print 'wrote vid'

#### PORTION THAT RUNS
## Verbosity vars
V = True

## Image subtraction vars
ref = None 
xds = []
yds = []
xr = None
yr = None

## Decision vars
WINDOW = 10
BOUNDX = 200
BOUNDY = 200

## Recording Parameters
RES = (1080, 1080)
FR = 25

## Timing vars
VIDLEN = 20
start = time.time()

## Motor Control Board
ebb = easyEBB()


with picamera.PiCamera() as camera:
    camera.resolution = RES
    camera.framerate = FR
    stream = picamera.PiCameraCircularIO(camera, seconds = 10)
    camera.start_recording(stream, format = 'h264')
    
    try:
        now = time.time()
        while(start - now <= VIDLEN):
            if findWorm(camera):
                write_vid(stream)
    finally:
        camera.stop_recording()
        ebb.closeSerial()
        print 'done'
        