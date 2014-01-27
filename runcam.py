## edit
from easyCam import easyCam
import time

c = easyCam()
c.setVidRes(1080,1080)
c.setVidLen(20) #in secs
c.setVidName('test1')
c.setFrameRate(25) #in fps
c.setCapFreq(1) #in fps
c.setQuant(23)

#c.recordVidCapStills()
c.threadStream()
#c.recordVid()
