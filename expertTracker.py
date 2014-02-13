#!/usr/bin/python

import threading #look Ma! I'm multi-threaded :)
import time #for timeing and stuff
import io #for streams
from PIL import Image #for reading in images
import numpy as np #for matrix maths
import picamera #connexion to camera


### Wouldn't be a Valerie program unless I had allllllll these globals :)
## General
V = True #If true, tons of print statements
START = time.time()

## Threading
exitFlag = 0

## Worm-finding
WINDOW = 10
VIDLEN = 120
VIDNAME = 'mttest1.h264' 
BOUNDROW = 200
BOUNDCOL = 200

'''
Runs the worm thread
'''
class wormThread ( threading.Thread ):
    def __init__( self, threadID, name, picStream ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.name = name
        #self.picStream = picStream
        self.camera = picStream

    def run( self ):
        print '%s\t%s\tStarting' % ( time.ctime(time.time()), self.name )
        findWorm( self.name, self.camera )
        print '%s\t%s\tExiting' % ( time.ctime(time.time()), self.name )
        

class writeThread ( threading.Thread ):
    def __init__( self, threadID, name, stream, delay ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.name = name
        self.stream = stream
        self.delay = delay

    def run( self ):
        print '%s\t%s\tStarting' % ( time.ctime(time.time()), self.name )
        writeVid( self.name, self.stream, self.delay )
        print '%s\t%s\tExiting' % ( time.ctime(time.time()), self.name )



'''
Finds the worm
TODO: Optimization 
TODO: sampling var, but realistically RPi won't be able to do this fast enough for us to specify this unless it's > 3 seconds
'''

def findWorm(threadName, stream):
    # Keep doing this until VIDEO is DONE
    ref = None
    colr = None
    rowdist = []
    coldist = []

    
    while time.time() - START <= 20: #!EXITF :     
        
        if exitFlag:
            thread.exit()
        
        # Capture image from cameraObj
        #        picStream = io.BytesIO()
        #        print '%s\t%s\tpicStream' % ( time.ctime( time.time() ), threadName )
        #        camObj.capture( picStream, format = 'jpeg', use_video_port = True )
        #        print '%s\tpast cam obj' % ( time.ctime( time.time() ), threadName )
        streamLock.acquire()
        stream.seek(0)
        
        if ref is None: #then camera has moved or we just got started
            
            if V: "New Reference frame acquired"
            #print stream
            ref = rgb2grayV( Image.open( stream ) )#.astype(float) #get image, mk gray, as float
            streamLock.release()
        else: #we already have a reference!
            if V: "New Comparison frame acquired"
            comp = rgb2grayV( Image.open( stream ) )#.astype(float)
            sub = comp - ref
            streamLock.release()
            #Find the maximum gray scale values -- corresponds to COMPARISON WORM (note: returns an array)
            col, row = np.nonzero( sub == sub.max() )
            
            # Find the minimum gray scale values -- corresponds to REFERENCE WORM
            if colr is None: #only process the reference image first time 'round
                if V: print 'Getting Maximum'
                colr, rowr = np.nonzero( sub == sub.min() )

            # For 'windowing' only consider a window of distances when making decision about whether or not to move
                #smoothes the location of the worm 
            coldist.append(colr[0] - col[0]) #arrays cuz np.nonzero returns all indices of maxima/minima in image
            rowdist.append(rowr[0] - row[0])
            
            if len(coldist) > WINDOW:
                #coldist.pop(0)
                #rowdist.pop(0)
                coldist = coldist[1:]
                rowdist = rowdist[1:]
            
            mcol = np.mean(coldist)
            mrow = np.mean(rowdist)
            
            if abs(mrow) > BOUNDROW or abs(mcol) > BOUNDCOL:
                print 'Move! row: %d \t col: %d' % ( rowdist[ len( rowdist ) - 1 ] , coldist [ len( coldist ) - 1 ] ) 
                ref = None; #triggers getting new reference image
                colr = None; #triggers getting new reference row/col position
            
    #finally:
     #   print 'have worm'
'''
def writeVid(threadName, stream, delay):
    while time.time() - START <= VIDLEN:
        print '%s\t%s\twriting vid' % ( time.ctime( time.time() ), threadName )
        with stream.lock:
            print '%s\t%s\tpast stream.lock' % ( time.ctime( time.time() ), threadName )
            for frame in stream.frames:
                print '%s\t%s\tframe' % ( time.ctime( time.time() ), threadName )
                if frame.header:
                    print '%s\t%s\tframe.header' % ( time.ctime( time.time() ), threadName )
                    stream.seek(frame.position)
                    print '%s\t%s\tpast stream seek' % ( time.ctime( time.time() ), threadName )
                    break

        with io.open(VIDNAME, 'wb') as output:
            print '%s\t%s\t past io.open' % ( time.ctime ( time.time() ), threadName )
            output.write( stream.read() )
            print '%s\t%s\tpast io write' % ( time.ctime( time.time() ), threadName )
        
        print '%s\t%s\tsleeping'  % ( time.ctime( time.time() ), threadName )
        time.sleep(delay)
               
    exitFlag = 1
'''
#def capFrames(threadName, stream, delay):
#    while time.time() <= VIDLEN:
        

### Helper helpers
def rgb2grayV(I):
    I = np.array(I) 
    I = I.astype( float )
    return 1.0/3 * ( I[:,:,0] + I[:,:,1] + I[:,:,2] )
    


### Actual main method
streamLock = threading.Lock()
with picamera.PiCamera() as camera:

    camera.resolution = (1080, 1080)
    camera.framerate = 25
    camera.start_recording('test.h264')
        # Capture image from cameraObj
    picStream = io.BytesIO()
#    print '%s\t%s\tpicStream' % ( time.ctime( time.time() ), threadName )

    camera.capture( picStream, format = 'jpeg', use_video_port = True )    
    wormT = wormThread(1, 'wormworm',  picStream  ) 
    try:
        
        wormT.start()
        while time.time() - START < VIDLEN:
            camera.capture( picStream, format = 'jpeg', use_video_port = True )
            time.sleep(2)
    except Exception as e:
        print str(e)
 
    finally:
        camera.stop_recording()
    
