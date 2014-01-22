"""
Created on Wed Dec 04 21:53:29 201
@author: Valerie
"""

from skimage import io, morphology, exposure,util
from skimage.measure import regionprops
#import matplotlib.pyplot as plt
import numpy as np

class imgProc:
      def __init__():
            
      def applyThresh( self, imgIn, t ):
      	  imgIn1 = imgIn.ravel()
	  imgOut = np.zeros( ( np.shape(imgIn) ) ).ravel()
	  inds = np.arange( len(imgIn1) )[imgIn1 > t]
	  for ind in inds:
	      imgOut[ind] = 1
    	      imgOut = np.reshape( imgOut, np.shape(imgIn) )
    	  return imgOut

      def threshAUHist( self, imgIn, avg, sd ):
          pxCnt, gL = exposure.histogram( imgIn )
          auh = 0
          gli = 0 #index into pxCnt and gL
          
          while( auh < avg + sd ):
              auh += pxCnt[gli]
              gli += 1
              t = gL[gli-1]
          
          imgOut = applyThresh( imgIn, t )
          return imgOut

      def morphOps( self, imgIn, sizeSE ):
          imgOut = util.img_as_bool( imgIn ) #boolean image
          imgOut = ~imgOut #img negative
          imgOut = morphology.remove_small_objects( imgOut, 2000 ) #largest cc
          SE = morphology.selem.disk( sizeSE ) #structuring element
          imgOut = morphology.closing(imgOut, SE)
          return imgOut

      def getCentroid( self, imgIn ):
          imgInL = morphology.label( imgIn )
          regions = regionprops( imgInL )
          y,x = regions[0]['Centroid']
          return x, y
    
## Sample run   
#J = threshAUHist(I, 4223, 19)
#J = morphOps(J,3)
#x, y = getCentroid(J)
#print x, y
#io.imshow(J)
