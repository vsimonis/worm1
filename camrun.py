from easyCam import easyCam

c = easyCam()
c.setVidRes(800,600)
c.setVidLen(0.5)
c.setVidName('test')

c.recordVid()
