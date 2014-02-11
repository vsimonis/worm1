'''
Created on Feb 6, 2014

@author: Valerie
'''
import io
import time
#import picamera
#from imgProc import imgProc
#from PIL import Image
import matplotlib
matplotlib.use("Agg")
from skimage import io as skio
from skimage import color
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

#import threading
#from easyEBB import easyEBB
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
    

DURATION = 1000; #in ms
STEPX = 1/100 #pixels per step
STEPY = 1/100 #pixels per step
BOUNDX = 200; #pixels
BOUNDY = 200; #pixels
VIDLEN = 600; #in sec
PING = 0.5; #in sec
WINDOW = 10; #number of frames to average
i = 0
DPI = 800;
XPI = 1080
YPI = 1080

cap = cv2.VideoCapture('C:\\Users\\vsimonis\\Documents\\MATLAB\\WormTracker\\Media\\led_move1.avi')
#ret, frame = cap.read()

FFMpegWriter = animation.writers['ffmpeg']
metadata = dict(title='Estimating Worm', artist='Matplotlib',
        comment='All maxima-minima, 200 bound, new refs, flipx-y 300 s')
writer = FFMpegWriter(fps=30, metadata=metadata)

fig = plt.figure(dpi = DPI)

startT = time.time() # start time
lastCheck = startT - PING # artificial last check
now = startT
ref = None;
#print "size ref: %d" % np.size(ref)
xds = [];
yds = [];
xr = 0;
yr = 0;
#print 'read'
#try: 
with writer.saving(fig, "writer_test10.mp4", 100):
    while True:
        now = time.time()
        #camera.wait_recording(1)
        if now - lastCheck >= PING:
            #print 'new image'
        #print 'read'
            ret, frame = cap.read()
        #    t = tic()
            lastCheck = time.time()
            #camera.capture(stream2, format='jpeg', use_video_port = True)
            #stream2.seek(0)
            #img = frame[:,:,1]
        #print 'rgbGray'
            img = rgb2grayV(frame).astype(float)
            if np.size(ref) == 1:
            #print 'new REFERENCE'
                #print 'new ref'
                ref = img;
                pass
            else: 
                #print 'img SUBTRACTION'
                sub = img - ref.astype(float)
                x, y = np.nonzero(sub == np.max(sub))
                xr, yr = np.nonzero(sub == np.min(sub))
    
                    #i = np.argmin(sub)
                    #print i
                    #s = (np.size(sub, 0), np.size(sub,1))
                    #print s
                    #j = np.argmax(sub)
                   # print j
                    #x, y = np.unravel_index(i, s)
                    #x, y = np.unravel_index(j, s)
                    
                    #print "x:\t%d\ty:\t%d" % (x, y)
                    #print "xr:\t%d\tyr:\t%d" % (xr, yr)
    
                xds.append(x[0] - xr[0] )
                yds.append(y[0] - yr[0] )
                #print 'plot'
                fig.clf()
                ip = plt.imshow(sub, cmap = 'gray')
                ip.set_clim(sub.min(), sub.max())
                plt.scatter(y, x, c = 'r')
                plt.scatter(yr, xr, c = 'b')
                    #plt.show()
                    #print xds
                    #print yds
                    #print "len: %d" % len(xds)
                if (len(xds) > WINDOW):
                    xds.pop(0)
                    yds.pop(0)
                #print 'update means'
                #print xds
                #print yds
                mx = np.mean(xds)
                my = np.mean(yds)
                #print "mean x: %d y: %d" % (mx, my)    
               
                if abs(mx) > BOUNDX or abs(my) > BOUNDY:
                    #print "MOVE %d, %d" % (mx, my)
                    #print sub
                    #plt.clf()
                    #plt.imshow(sub, cmap = 'gray')
                    #plt.scatter(x, y, c = 'r')
                    #plt.scatter(xr, yr, c = 'b')
                    ref = None
                #print 'write frames'
                writer.grab_frame()
                    #plt.show()
                    #ref = None
                #print "time: %f s" % toc(t)
                print 'time elapsed: %f' % (now - startT)
                if (now - startT >= VIDLEN) or ret == False:
                    print 'time elapsed: %f' % (now - startT)

                    print 'end video'
                    #cap.close()
                    sys.exit()


