import picamera
import io
import time
from PIL import Image

class medCam:
    def __init__( self, vidlen, res, fr, caprate ):
        self.VidLen = vidlen
#        print self.VidLen
        self.VidRes = res
#        print self.VidRes
        self.FrameRate = fr
#        print self.FrameRate
        self.SampleRate = caprate
#        print self.SampleRate
#        self.Stream = io.BytesIO()

    def proc_write_vid( stream ):
        with stream.lock:
            try:
                for frame in stream.frames:
                    if frame.header:
                        stream.seek(frame.position)
                        print 'process'
                        img = Image.open(stream)
                        [x, y] = imgProc.getCentroidFromRaw(img)
                        print "x: %d \ty: %d" % (x, y)
                        break
                print 'write'    
                with io.open('test1.h264', 'wb') as output:
                    output.write(stream.read())
                    #while True:
                    #    buf = self.Stream.read1()
                    #    if not buf:
                    #        break
            finally:
                return

    def cap( self ):
        
        capInterval = float(1)/self.SampleRate
        print capInterval
        with picamera.PiCamera() as cam:
            print 'here'
            stream = picamera.PiCameraCircularIO(cam, seconds = 10)
            cam.resolution = self.VidRes
            print cam.resolution
            cam.framerate = self.FrameRate
            print cam.framerate
            cam.start_preview()
            time.sleep(2)
            camera.start_recording(stream, format='h264')
            startT = time.time()          
            lastCheck = startT - capInterval
            now = time.time()
            while now - startT >= self.VidLen:
                now = time.time()
                if now - lastCheck >= capInterval:
                    lastCheck = time.time()
                    proc_write_vid(stream)
            camera.stop_recording()
