import picamera
import time
from datetime import datetime
class easyCam:
    def __init__( self ):
        self.vidRes = None    #(x, y) tuple
        self.frameRate = None   #frames per second
        self.capFreq = None #images per second
        self.vidLen = None #expressed in seconds

    ## Set parameters for video capture
    # Resolution
    def setVidRes( self, x, y ):
        self.vidRes = ( x, y )
    
    def setVidLen( self, vidLength ):
        self.vidLen = vidLength
        print "set vidLen: %d" % self.vidLen

    # Frame Rate    
    def setFrameRate( self, fRate ):
        self.frameRate = fRate
    
    def setVidName( self, vidNm ):
        self.vidName = vidNm

    ## Set parameters for query images sent to image processor
    # Capture frequency expressed in image queries per min
    def setCapFreq( self, freq):
        self.capFreq = freq
        print "set capFreq: %d" % self.capFreq
   
    ## Recording Methods    
    def recordVid( self ):
        with picamera.PiCamera() as camera: 
            if self.vidRes == None:
                print 'set vidRes'
            if self.vidLen == None:
                print 'set vidLen'
            if self.vidName == None:
                print 'set vidName'            
            else :
                camera.resolution = self.vidRes
                camera.framerate = self.frameRate
                camera.start_recording( '%s.h264' % self.vidName )
                camera.wait_recording( self.vidLen * 60 )
                camera.stop_recording()

    def pingImg ( self ):
        with picamera.PiCamera() as camera:
            camera.resolution = self.vidRes
            camera.start_preview()
            time.sleep(2)
            camera.capture('\pics\%s.jpg' % str( datetime.now() ))


    def recordVidCapStills ( self ):
        nCap = self.vidLen * self.capFreq
        print "vid Len Still: %d" % self.vidLen
        print "capFreq Still: %d" % self.capFreq
        print "nCap: %d" % nCap
        with picamera.PiCamera() as camera:
            camera.resolution = self.vidRes
            camera.framerate = self.frameRate
            camera.start_preview()
            camera.start_recording( '%s.h264' % self.vidName )
            i = 0
            while i < nCap - 1:             
                print i
                camera.wait_recording(self.vidLen // nCap)
                camera.capture('\pics\%s.jpg' % str( datetime.now() ), use_video_port = True)
                i += 1
            camera.wait_recording( self.vidLen // nCap)
            camera.stop_recording()
    
