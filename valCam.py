import io
import time
import picamera
from imgProc import imgProc
#from PIL import Image
from skimage import io as skio
import threading

def get_frame(stream):
    for frame in stream.frames:
        if frame.header:
            stream.seek(frame.position)
        return (frame.frame_size, frame.position)

def write_video( stream, img ):
    print ('writing video')
    #stream2 = io.BytesIO()
    with stream.lock:
        #(ksize, kpos) = get_frame(stream)# Find keyframe
        for frame in stream.frames:
            if frame.header: #is keyframe
                stream.seek(frame.position)
                break
         
        # write rest of stream to disk
        with io.open('test1.h264','wb') as output:
            output.write(stream.read())
        
        # process
        #img = Image.open(stream.read1(frame.frame_size)) 
        x, y = imgProc.getCentroidFromRaw(img)
        print "x: %d\ty: %d"%(x,y)
        
with picamera.PiCamera() as camera:
    stream = picamera.PiCameraCircularIO(camera, seconds = 20)
    stream2 = io.BytesIO()
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
                camera.capture(stream2, format='jpeg', use_video_port = True)
                stream2.seek(0)
                img = skio.imread(stream2)
                write_video(stream, img)
    finally:
        camera.stop_recording()
    
