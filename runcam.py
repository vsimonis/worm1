## edit
from easyCam import easyCam
import time

c = easyCam()
c.setVidRes(800,600)
c.setVidLen(20) #in secs
c.setVidName('test')
c.setFrameRate(10) #in fps
c.setCapFreq(1) #in fps

c.recordVidCapStills()
