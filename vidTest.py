##stackoverflow.com/questions/10672578/extract-video-frames-in-python
import cv2
from imgProc import imgProc as ipr
import matplotlib.pyplot as plt
from skimage import color, exposure, io
import numpy as np
vid = 'C:\\Users\\vsimonis\\Downloads\\led_tests\\led_move1.avi'


vc = cv2.VideoCapture(vid)
c = 1

i = 1 
modulus = 50

if vc.isOpened():
    rval, frame = vc.read()
else: 
    rval = False
'''    
plt.figure()
io.imshow(frame)
plt.show()
'''

gframe = color.rgb2gray(frame)

'''
plt.figure()
io.imshow(gframe)
plt.show()
'''

#J = ipr.minmaxx(gframe)

I = ipr.threshHist(gframe)

plt.figure()
io.imshow(I)
plt.show()
#ipr.getCentroidFromRaw(frame)






'''
imgIn1 = gframe.ravel()
#imgOut = np.zeros( (np.shape(imgIn) ) ).ravel()
# Histogram analysis to find maximum peak and associated gl
pxCnt, gL = exposure.histogram( gframe )
indMaxBG = int(np.arange( len(imgIn1) )[pxCnt == max(pxCnt)]) #int()
BGlevel = gL[indMaxBG]

# Nearest min below this max is threshold 
d1 = np.zeros( np.shape(pxCnt) )
  
for i in range( 2 , len(pxCnt) - 1):
    # derivative approximation
    d1[i] = pxCnt[ i + 1 ] - pxCnt[ i ]

i = 1
p = 0

while ( d1[ indMaxBG - i ] > 0): ### - i!!!
    p = indMaxBG - i
    print p
    i = i + 1

t = gL[ p ]


imgIn1 = gframe.ravel()
imgOut = np.zeros( ( np.shape(gframe) ) ).ravel()
inds = np.arange( len(imgIn1) )[imgIn1 > t]
for ind in inds:
    imgOut[ind] = 1
imgOut = np.reshape( imgOut, np.shape(gframe) )
return imgOut

#imgOut = ipr.applyThresh( gframe , t ) 
 
"""while rval: 
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
"""
'''

