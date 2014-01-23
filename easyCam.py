import picamera
import time
from datetime import datetime
import io
import sys
from select import select


class easyCam:
    def __init__( self ):
        self.vidRes = None    #(x, y) tuple
        self.frameRate = None   #frames per second
        self.sampleRate = None #images per second
        self.vidLen = None #expressed in seconds
        self.quant = None

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
        
    # Quantization
    def setQuant(self, q ):
        self.quant = q

    ## Set parameters for query images sent to image processor
    # Capture frequency expressed in image queries per min
    def setCapFreq( self, freq):
        self.capFreq = freq
        print "set sampleRate: %d" % self.sampleRate
   
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

    def pingImg( self ):
        with picamera.PiCamera() as camera:
            camera.resolution = self.vidRes
            camera.start_preview()
            time.sleep(2)
            camera.capture('\pics\%s.jpg' % str( datetime.now() ))


    def recordVidCapStills( self ):
        nCap = self.vidLen * self.sampleRate
        print "vid Len Still: %d" % self.vidLen
        print "sampleRate Still: %d" % self.sampleRate
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
    
    def recordStream( self ):
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.resolution = self.vidRes
            camera.framerate = self.frameRate
            camera.start_preview()
            camera.start_recording( stream, self.quant)
            camera.wait_recording( self.vidLen )
            camera.stop_recording()
            
    def threadStream( self ):
        nCap = self.vidLen * self.sampleRate

        with picamera.PiCamera() as camera:
            camera.resolution = self.vidRes
            camera.framerate = self.frameRate
            stream = picamera.PiCameraCircularIO(camera, seconds = 10)
            camera.start_recording(stream, format = 'h264')
            
            i = 0
            while i < nCap - 1:             
                print i
                camera.wait_recording(self.vidLen // nCap)
                with stream.lock:
                    for frame in stream.frames:
                        if frame.header:
                            img = stream.seek(frame.position)
                            print 'img'
                            break
                i += 1
                with io.open( '%s.h264' % self.vidName, 'wb' ) as output:
                    while True:
                        buf = stream.read1()
                        if not buf:
                            break
                        output.write(buf)
            camera.wait_recording( self.vidLen // nCap)
            camera.stop_recording()
                
