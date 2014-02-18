import picamera
import time
from easyEBB import easyEBB

R = False

e = easyEBB()


SLP = 2

duration = 60
x = 7
y = 7
fr = 30
res = (600, 600)

fname = 'dur%d-x%d-y%d-fr%d-res-%s.h264' % (duration, x, y, fr,  str(res) )

with picamera.PiCamera() as cam:

    cam.framerate = fr
    cam.resolution = res
    cam.start_preview()
    
    
    if R:
        time.sleep(SLP)
        cam.start_recording(fname)

        try:
            e.stepM(duration, x, y)
            time.sleep(SLP)
    
            e.stepM(duration, -x, -y)
            time.sleep(SLP)        

        finally:
            e.closeSerial()  
            cam.stop_recording()
            cam.stop_preview()    
            cam.close()
    else:
        time.sleep(20)
        cam.stop_preview()    
        cam.close()
