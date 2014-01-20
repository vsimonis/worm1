import picamera
import time

class easyCam:
    def __init__( self ):
        self.videoRes = None    #(x, y) tuple
        self.frameRate = None   #frames per second
        self.captureFreq = None #images per minute
        self.vidLength = None #expressed in minutes

    ## Set parameters for video capture
    # Resolution
    def setVideoRes( self, x, y ):
        self.videoRes = ( x, y )

    # Frame Rate    
    def setFrameRate( self, fRate ):
        self.frameRate = fRate

    ## Set parameters for query images sent to image processor
    # Capture frequency expressed in image queries per min
    def setCaptureFreq( self, freq):
        self.captureFreq = freq
    
    def setVidLength


 
    
