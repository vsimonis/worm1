#!/usr/bin/python
from easyEBB import easyEBB

e = easyEBB()

e.stepM(1000,300,0)
e.stepM(1000,0,300)
e.stepM(1000,-300,0)
e.stepM(1000, 0, -300)

e.closeSerial()
