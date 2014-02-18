### Main
import numpy as np
import picamera
import threading
import io
import time
from PIL import Image
V = True
P = True
exitFlag = 0;
res = (1080, 1080)
 
### Helper helpers
def rgb2grayV(I):
    I = np.array(I) 
    I = I.astype( float )
    return 1.0/3 * ( I[:,:,0] + I[:,:,1] + I[:,:,2] )
    



class stillThread ( threading.Thread ):
    def __init__( self, threadID, name, camera ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.name = name
        self.camera = camera

    def run( self ):
        counter = 1
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
        recordVideo( self.name, self.camera, VIDLEN )
        print '%s\t%s\tExiting' %  ( time.ctime( time.time() ) , self.name )
        

def recordVideo ( threadName, camera, vidLen ):
    print '%s\t%s\tCamera\t%s' %  ( time.ctime( time.time() ) , threadName, str(camera) )

        #vidStream = picamera.PiCameraCircularIO(self.camera, seconds = 10)
        #camera.start_recording( vidStream, format = 'h264') #stream
    try: 
        camera.start_preview()
        camera.start_recording('testMT.h264')
        camera.wait_recording(vidLen)
    except Exception as e:
        print str( e )
    finally:
        print '%s\t%s\tStop Recording' %  ( time.ctime( time.time() ) , threadName )                              
        camera.stop_recording()
    
def findWorm ( threadName, camera ):
    
    
    if P: camera.start_preview()
###
    ref = None
    colr = None
    rowdist = []
    coldist = []
    #print V
    start = time.time()
    ###
    camera.resolution = res

    stillStream = io.BytesIO()        
    while time.time() - start <= VIDLEN:
        print '%s\t%s\tcapture' %  ( time.ctime( time.time() ) , threadName )
        camera.capture( stillStream, format = 'jpeg', use_video_port = True )
        print '%s\t%s\tsleep' % ( time.ctime( time.time() ) , threadName )

#####
        stillStream.seek(0)
        if ref is None: #then camera has moved or we just got started
            
            if V: print '%s\t%s\tHave new reference' %  ( time.ctime( time.time() ) , threadName )
            #print stream
            ref = rgb2grayV( Image.open( stillStream ) )#.astype(float) #get image, mk gray, as float
            stillStream.seek(0)
            stillStream.truncate()
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

    if P: camera.stop_preview()





#        time.sleep(5);
        
       
############ RUN ###############

#with picamera.PiCamera() as camera:
camera = picamera.PiCamera() 
video = videoThread( 1, 'video', camera )
stills = stillThread( 2, 'still', camera )
VIDLEN = 30

try:
    #video.start()
    stills.start()
except Exception as e:
    print str(e)
#finally:
    #camera.stop_recording()
    




