##stackoverflow.com/questions/10672578/extract-video-frames-in-python
import cv2
from imgProc import imgProc as ipr
import matplotlib.pyplot as plt
vid = 'led_move1.avi'

vc = cv2.VideoCapture(vid)
c = 1

i = 1 
modulus = 50

if vc.isOpened():
    rval, frame = vc.read()
else: 
    rval = False

while rval: 
    rval, frame = vc.read()
    if i % 10 == 0:
        x, y = ipr.getCentroidFromRaw(frame)
        print x, y
        plt.figure()
        plt.imshow(frame)
        plt.show()
    cv2.waitKey(1)
    i += 1
vc.release()
