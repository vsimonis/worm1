#!/usr/bin/python

import threading #look Ma! I'm multi-threaded :)
import time #for timeing and stuff
import io #for streams
from PIL import Image #for reading in images
import numpy as np #for matrix maths
import picamera #connexion to camera
import matplotlib.pyplot as plt
import random 


### Wouldn't be a Valerie program unless I had allllllll these globals :)
## General
V = True #If true, tons of print statements
P = False #If true, display matplotlib plots, need to be running startX
R = False

START = time.time()

VIDLEN = 10
VIDRES = (1080,1080)
VIDFR = 15

## Worm-finding
WINDOW = 10
VIDNAME = 'mttest1.h264' 
BOUNDROW = 400
BOUNDCOL = 400

'''
Runs the worm thread
'''

class stillThread ( threading.Thread ):
    def __init__( self, threadID, name, camera ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.name = name
        self.camera = camera

    def run( self ):
        print '%s\t%s\tStarting' %  ( time.ctime( time.time() ) , self.name )
        findWorm ( self.name, self.camera )
        print '%s\t%s\tExiting' %  ( time.ctime( time.time() ) , self.name )
        

class videoThread ( threading.Thread ):
    def __init__( self, threadID, name, camera ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.name = name
        self.camera = camera
        
    def run( self ):
        print '%s\t%s\tStarting' %  ( time.ctime( time.time() ) , self.name )
        recordVideo( self.name, self.camera )
        print '%s\t%s\tExiting' %  ( time.ctime( time.time() ) , self.name )
        
def write_video ( threadName, vidStream ):   
    with vidStream.lock:
        for frame in vidStream.frames:
            if frame.header:
                vidStream.seek(frame.position)
                break
        print '%s\t%s\twriting' %  ( time.ctime( time.time() ) , threadName )
        with io.open(VIDNAME, 'wb') as output:
            output.write( vidStream.read() )

def write_now( ):
    return random.randint(0,10) == 0

def recordVideo ( threadName, camera ):
    start = time.time()
    print '%s\t%s\tCamera\t%s' %  ( time.ctime( time.time() ) , threadName, str(camera) )
    if not V: camera.start_preview()
    vidStream = picamera.PiCameraCircularIO(camera, seconds = 10)
    camera.start_recording( vidStream, format = 'h264') #stream
    #try:
    while time.time() - start <= VIDLEN:
        camera.wait_recording( 5 )
        print '%s\t%s\twrite now' % ( time.ctime(time.time() ), threadName)
        write_video( threadName, vidStream )
    camera.stop_recording()
    print '%s\t%s\tStop Recording' %  ( time.ctime( time.time() ) , threadName )                              


'''
Finds the worm
TODO: Optimization 
TODO: sampling var, but realistically RPi won't be able to do this fast enough for us to specify this unless it's > 3 seconds
'''
def findWorm(threadName, camera):
    if not R: 
        camera.start_preview()
        time.sleep(2)

    # Keep doing this until VIDEO is DONE
    ref = None
    colr = None
    rowdist = []
    coldist = []
    #print V
    start = time.time()

    stillStream = io.BytesIO()        
    while time.time() - start <= VIDLEN:
        print '%s\t%s\tcapture' %  ( time.ctime( time.time() ) , threadName )
        camera.capture( stillStream, format = 'jpeg')#, use_video_port = True)
        stillStream.seek(0)
    if not R: 
        camera.stop_preview()
'''   
        if ref is None: #then camera has moved or we just got started
            
            if V: print '%s\t%s\tHave new reference' %  ( time.ctime( time.time() ) , threadName )
            #print stream
            ref = rgb2grayV( Image.open( stillStream ) )#.astype(float) #get image, mk gray, as float
            stillStream.seek(0)
            stillStream.truncate()
            #if P:
                #ip = plt.imshow(ref, cmap = 'gray')
                #ip.set_clim(np.min(ref), np.max(ref))
                #plt.show()
        else: #we already have a reference!
            comp = rgb2grayV( Image.open( stillStream ) )#.astype(float)
            stillStream.seek(0)
            stillStream.truncate()
            if V: print '%s\t%s\tHave comparison' %  ( time.ctime( time.time() ) , threadName )

            sub = comp - ref
            if V: print '%s\t%s\tHave subtraction' %  ( time.ctime( time.time() ) , threadName )
            #Find the maximum gray scale values -- corresponds to COMPARISON WORM (note: returns an array)
            

            col, row = np.nonzero( sub == np.max(sub) )
            if V: print '%s\t%s\tHave maximum\t%d\trow:%d\tcol:%d' %  ( time.ctime( time.time() ) , threadName, np.max(sub), row[0], col[0] )
            
            # Find the minimum gray scale values -- corresponds to REFERENCE WORM
            if colr is None: #only process the reference image first time 'round
                colr, rowr = np.nonzero( sub == np.min(sub) )
                if V: print '%s\t%s\tHave minimum\t%d\trow:%d\tcol:%d' %  ( time.ctime( time.time() ) , threadName, np.min(sub), rowr[0], colr[0] )


            if P:
                camera.stop_preview()
                try:
                    #ip = plt.imshow(sub, cmap = 'gray')
                    plt.imshow(sub, cmap = 'gray')
                    #ip.set_clim(np.min(sub), np.max(sub))
                    plt.scatter(row, col, c = 'r')
                    plt.scatter(rowr, colr, c = 'c')
                    plt.show()                    
                finally:
                    camera.start_preview()

            # For 'windowing' only consider a window of distances when making decision about whether or not to move
                #smoothes the location of the worm 
            coldist.append(colr[0] - col[0]) #arrays cuz np.nonzero returns all indices of maxima/minima in image
            rowdist.append(rowr[0] - row[0])
            if V: print '%s\t%s\tHave appended distance arrays' %  ( time.ctime( time.time() ) , threadName )
            
            if len(coldist) > WINDOW:
                #coldist.pop(0)
                #rowdist.pop(0)
                coldist = coldist[1:]
                rowdist = rowdist[1:]
                if V: print '%s\t%s\tHave sliced distance arrays' %  ( time.ctime( time.time() ) , threadName )
            
            mcol = np.mean(coldist)
            mrow = np.mean(rowdist)
            if V: print '%s\t%s\tHave mean distances:\trow:%d\tcol:%d' %  ( time.ctime( time.time() ) , threadName, mrow, mcol )
            
            if abs(mrow) > BOUNDROW or abs(mcol) > BOUNDCOL:
                print '%s\t%s\tMove! row: %d \t col: %d' % ( time.ctime( time.time() ) , threadName , rowdist[ len( rowdist ) - 1 ] , coldist [ len( coldist ) - 1 ] ) 
                ref = None; #triggers getting new reference image
                colr = None; #triggers getting new reference row/col position
'''
#if not R: camera.stop_preview()

### Helper helpers
def rgb2grayV(I):
    I = np.array(I) 
    I = I.astype( float )
    return 1.0/3 * ( I[:,:,0] + I[:,:,1] + I[:,:,2] )
    


### Actual main method
############ RUN ###############

#with picamera.PiCamera() as camera:
camera = picamera.PiCamera() 
video = videoThread( 1, 'video', camera )
stills = stillThread( 2, 'still', camera )
camera.resolution = VIDRES
camera.framerate = VIDFR

try:
    if R: video.start()
    stills.start()
except Exception as e:
    print str(e)

finally:
    if camera.recording:
        camera.stop_recording()
    camera.close()
