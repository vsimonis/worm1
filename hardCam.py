import io
import time
import threading
import picamera
from imgProc import imgProc
from PIL import Image
import random

#Pool of image processors
done = False
lock = threading.Lock()
pool = []

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # separate thread
        global done
        while not self.terminated:
            if self.event.wait(1):
                try: 
                    self.stream.seek(0)
                    img = Img.open(self.stream)
                    [x, y] = imgProc.getCentroidFromRaw(img) ##img processing
                    print "x: %d, y: %d" % (x,y)
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return to pool 
                    with lock: 
                        pool.append(self)
def streams():
    while not done:
        with lock:
            processor = pool.pop()
        yield processor.stream
        processor.event.set()

def write_now(): #Randomly returns true
    return random.randint(0,10) == 0

def write_vid(stream):
    print('write')
    with stream.lock:
        #Find header frame 
        for frame in stream.frames:
            if frame.header:
                stream.seek(frame.position)
                break

        with io.open('test1.h264', 'wb') as output:
            output.write(stream.read1())


with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range (4)]
    #camera.resolution = #set resolution
    #camera.framerate = #set framerate
        
    camera.start_preview()
    time.sleep(2)
    camera.capture(streams(), format = 'h264')
    try: 
        while True: 
            camera.wait_recording(1)
            if write_now():
                camera.wait_recording(10)
                write_vid(stream)
    finally:
        camera.stop_recording()
        

    #shut it down
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
        
                    
