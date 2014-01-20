import picamera
import time
from datetime import datetime
class easyCam:
    def __init__( self ):
        self.vidRes = None    #(x, y) tuple
        self.frameRate = None   #frames per second
        self.capFreq = None #images per minute
        self.vidLen = None #expressed in minutes

    ## Set parameters for video capture
    # Resolution
    def setVidRes( self, x, y ):
        self.vidRes = ( x, y )
    
    def setVidLen( self, vidLength ):
        self.vidLen = vidLength

    # Frame Rate    
    def setFrameRate( self, fRate ):
        self.frameRate = fRate
    
    def setVidName( self, vidNm ):
        self.vidName = vidNm

    ## Set parameters for query images sent to image processor
    # Capture frequency expressed in image queries per min
    def setCapFreq( self, freq):
        self.capFreq = freq
    
   
    ## Recording Methods    
    def recordVid( self ):
        with piCamera() as camera: 
            if self.vidRes or self.vidLen or self.vidName == None:
                print "Please set a resolution, video length or name"
            
            else :
                camera.resolution = self.vidRes
                camera.start_recording( '%s.h264' % self.vidName )
                camera.wait_recording( self.vidLen * 60 )
                camera.stop_recording()

    def pingImg ( self ):
        with piCamera() as camera:
            camera.resolution = self.vidRes
            camera.start_preview()
            time.sleep(2)
            camera.capture('%s.jpg' % str( datetime.now() ))



 
    
