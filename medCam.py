import picamera
import io
import time
from PIL import Image

class medCam:
    def __init__( self, vidlen, res, fr, caprate ):
        self.VidLen = vidlen
        self.VidRes = res
        self.FrameRate = fr
        self.SampleRate = caprate
        self.Stream = io.BytesIO()

    def proc_write_vid( self ):
        print 'process'
        with self.Stream.lock:
            try:
                for frame in self.Stream.frames:
                    if frame.header:
                        self.Stream.seek(frame.position)
                        img = Image.open(self.Stream)
                        [x, y] = imgProc.getCentroidFromRaw(img)
                        print "x: %d \ty: %d" % (x, y)
                        break
                
                with io.open('test1.h264', 'wb') as output:
                    output.write(self.Stream.read())
            #finally:
                

    def cap():
        capInterval = float(1)/self.SampleRate
        with picamera.PiCamera() as cam:
            cam.resolution = self.vidRes
            cam.framerate = self.FrameRate
            
            cam.start_preview()
            time.sleep(2)
            camera.capture(stream, format='h264')
            startT = time.time()          
            lastCheck = startT - capInterval
            now = time.time()
            while now - startT >= self.VidLen:
                now = time.time()
                if now - lastCheck >= capInterval:
                    lastCheck = time.time()
                    proc_write_vid()
            camera.stop_recording()
