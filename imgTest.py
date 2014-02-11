'''
Created on Jan 22, 2014

@author: VSIMONIS
'''
#import cv2
from imgProc import imgProc as ipr
import matplotlib.pyplot as plt
from skimage import color, exposure, io
#import numpy as np
import time

def tic():
    return time.time()
def toc(t):
    return time.time() - t

#for i in range(0,10):
I1 = io.imread('C:\\Users\\vsimonis\\Documents\\MATLAB\\Intro to Img Processing\\FinalProj\\Media\\ledtest-200.tif')


#I1 = ipr.cropBorder(I1, 0, 200)

io.imshow(I1)
plt.show()
t1 = tic()
J = ipr.threshHist(I1)
print "thresh runtime\t%f" % toc(t1)
io.imshow(J)
plt.show()
t2 = tic()
K = ipr.morphOps(J, 5, 1000)
print "morph runtime\t%f" % toc(t2)

plt.figure()
plt.imshow(K, cmap='gray')
t3 = tic()
x,y = ipr.getCentroid(K)
#plt.scatter(x, y)
print "centroid runtime\t%f" % toc(t3)
#print str(x) + " " + str(y)
plt.show()

t4 = tic()
ipr.getCentroidFromRaw(I1)
print "all runtime\t%f" % toc(t4)

t5 = tic()
ipr.all(I1)
print "all opt\t%f" % toc(t5)

print "\n"



