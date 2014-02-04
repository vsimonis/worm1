import io
import time
import picamera
import imgProc
from PIL import Image
import threading

#lock = threading.Lock()

def write_video( stream ):
    print ('writing video')
    with stream.lock:
        # Find keyframe
        for frame in stream.frames:
            if frame.header: #is keyframe
                stream.seek(frame.position)
                break
        # process
        img = Image.open(stream) 
        x, y = imgProc.getCentroidFromRaw(img)
        print "x: %d\ty: %d"%(x,y)
         
        # write rest of stream to disk
        with io.open('test1.h264','wb') as output:
            output.write(stream.read())

with picamera.PiCamera() as camera:
    #stream = picamera.PiCameraCircularIO(camera, seconds = 20)
    stream = io.BytesIO()
    camera.start_recording(stream, format='h264')
    startT = time.time() # start time
    lastCheck = startT - 1 # artificial last check
    now = startT
    try: 
        while now - startT <= 20: #while less than video length
            now = time.time()
            #camera.wait_recording(1)
            if now - lastCheck >= 1:
                lastCheck = time.time()
                write_video(stream)
                
    finally:
        camera.stop_recording()
    
