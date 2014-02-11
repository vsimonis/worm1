'''
Created on Feb 6, 2014

@author: Valerie
'''
import io
import time
import picamera
from skimage import io as skio
from skimage import color
import numpy as np
import sys
import threading
from easyEBB import easyEBB

RES = (1080, 1080)
FRAMERATE = 25 #in fps
DURATION = 1000; #in ms
STEPX = 1/100 #pixels per step
STEPY = 1/100 #pixels per step
BOUNDX = 200; #pixels
BOUNDY = 200; #pixels
VIDLEN = 20; #in sec
PING = 0.5; #in sec
WINDOW = 10; #number of frames to average
V = True;
ebb = easyEBB() 

def tic():
    return time.time()
def toc(t):
    return time.time() - t

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

#def write_video( stream, img ):
#    print ('writing video')
#    #stream2 = io.BytesIO()
#    with stream.lock:
#        #(ksize, kpos) = get_frame(stream)# Find keyframe
#        for frame in stream.frames:
#            if frame.header: #is keyframe
#                stream.seek(frame.position)
#                break
#         
#        # write rest of stream to disk
#        with io.open('test1.h264','wb') as output:
#            output.write(stream.read())
        
        # process
        #img = Image.open(stream.read1(frame.frame_size)) 
        #x, y = imgProc.getCentroidFromRaw(img)
        #print "x: %d\ty: %d"%(x,y)

def move(ebb, xx, yy):
    ebb.stepM(DURATION, xx*STEPX, yy*STEPY)
### RUNNING PARTS

with picamera.PiCamera() as camera:
#    stream = picamera.PiCameraCircularIO(camera, seconds = 20)
    stream2 = io.BytesIO()
    camera.framerate = FRAMERATE
    camera.resolution = RES
    camera.start_recording('test-DPU.h264')
    camera.start_preview()
    startT = time.time() # start time
    lastCheck = startT - PING # artificial last check
    now = startT
    ref = None;
    xds = [];
    yds = [];
    xr = 0;
    yr = 0;
    try: 
        while now - startT <= VIDLEN: #while less than video length
            now = time.time()
            #camera.wait_recording(1)
            if now - lastCheck >= PING:
                lastCheck = time.time()
                camera.capture(stream2, format='jpeg', use_video_port = True)
                stream2.seek(0)
                if V: print '1. rgb2gray'
                img = rgb2grayV(skio.imread(stream2)).astype(float) #Valerie's rgb2gray
                if np.size(ref) == 1: #maybe use shape instead??? 
                    if V: print '2.A ref img'
                    ref = img;
                    ### Maybe find this centroid here??? 
                else: ## Image subtraction
                    if V: print '2.1B sub img'
                    sub = img - ref.astype(float)
                    if V: print '2.2B find max'
                    x, y = np.nonzero(sub == np.max(sub))
                    if V: print '2.3B find min'
                    xr, yr = np.nonzero(sub == np.min(sub))  
                    if V: print '2.4B append dist x'
                    xds.append(x[0] - xr[0] )
                    if V: print '2.5B append dist y'
                    yds.append(y[0] - yr[0] )
                    print len(xds)
                    if (len(xds) > WINDOW):
                        if V: print '2.6BB1 pop dist x'
                        xds.pop(0)
                        if V: print '2.6BB2 pop dist y'
                        yds.pop(0)
                    if V: print '2.6B mean dist x'
                    mx = np.mean(xds)
                    if V: print '2.7B mean dist y'
                    my = np.mean(yds)
                    print 'x: %d y: %d' % (x[0], y[0])
                    print 'xr: %d yr: %d' % (xr[0], yr[0])
                    if abs(mx) > BOUNDX or abs(my) > BOUNDY:
                        print 'move'
                        move(ebb, mx, my)
                        print 'mx: %d my:%d' % ( mx, my ) 
                        ref = None;
#                write_video(stream, img)
    finally:
        camera.stop_recording()
        ebb.closeSerial()
        print 'done'
        sys.exit()

