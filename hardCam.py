import io
import time
import threading
import picamera
from imgProc import imgProc
from PIL import Image

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
                    
