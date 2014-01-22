"""
Created on Wed Dec 04 21:53:29 201
@author: Valerie
"""

from skimage import io, morphology, exposure, util, color
from skimage.measure import regionprops
#import matplotlib.pyplot as plt
import numpy as np

class imgProc:
      
      def __init__(self):
            pass

      @staticmethod
      def applyThresh( imgIn, t ):
            imgIn1 = imgIn.ravel()
            imgOut = np.zeros( ( np.shape(imgIn) ) ).ravel()
            inds = np.arange( len(imgIn1) )[imgIn1 > t]
            for ind in inds:
                  imgOut[ind] = 1
                  imgOut = np.reshape( imgOut, np.shape(imgIn) )
            return imgOut
      
      @staticmethod
      def threshHist( imgIn ):
            imgIn1 = imgIn.ravel()
            imgOut = np.zeros( (np.shape(imgIn) ) ).ravel()
            # Histogram analysis to find maximum peak and associated gl
            pxCnt, gL = exposure.histogram( imgIn )
            indMaxBG = np.arange( len(imgIn1) )[pxCnt == max(pxCnt)]
            BGlevel = gL[indMaxBG]
            
            # Nearest min below this max is threshold
            
            d1 = np.zeros( np.shape(pxCnt) )
            
            for i in range( 2 , len(pxCnt) - 1):
                  # derivative approximation
                  d1[i] = pxCnt[ i + 1 ] - pxCnt[ i ]
            
            i = 1
            p = 0
            while ( d1[ indMaxBG ] > 0):
                  p = indMaxBG - i
                  i = i + 1
            t = gL[ p ]
            imgOut = imgProc.applyThresh( imgIn, t ) 
            return imgOut
      
      @staticmethod            
      def threshAUHist( imgIn, avg, sd ):
            pxCnt, gL = exposure.histogram( imgIn )
            auh = 0
            gli = 0 #index into pxCnt and gL
          
            while( auh < avg + sd ):
                auh += pxCnt[gli]
                gli += 1
                t = gL[gli-1]
          
            imgOut = imgProc.applyThresh( imgIn, t )
            return imgOut

      @staticmethod
      def morphOps( imgIn, sizeSE ):
            imgOut = util.img_as_bool( imgIn ) #boolean image
            imgOut = ~imgOut #img negative
            imgOut = morphology.remove_small_objects( imgOut, 2000 ) #cclargest
            SE = morphology.selem.disk( sizeSE ) #structuring element
            imgOut = morphology.closing(imgOut, SE)
            return imgOut

      @staticmethod
      def getCentroid( imgIn ):
            imgInL = morphology.label( imgIn )
            regions = regionprops( imgInL )
            y,x = regions[0]['Centroid']
            return x, y

      @staticmethod
      def getCentroidFromRaw( imgIn ):
            imgOut = color.rgb2gray( imgIn )
            imgOut = imgProc.threshHist( imgOut )
            x, y = imgProc.getCentroid( imgOut )
            return x, y
## Sample run   
#J = threshAUHist(I, 4223, 19)
#J = morphOps(J,3)
#x, y = getCentroid(J)
#print x, y
#io.imshow(J)