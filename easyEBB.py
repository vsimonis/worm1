#!/usr/bin/python

import pyserial
import time
import eggbot_scanlinux

class easyEBB:
    def __init__( self ):
        self.actualSerialPort = ''
        self.openSerial()

    def openSerial( self ):
        self.serialPort = self.getSerialPort()
        if self.serialPort == None:
            print "Unable to find serial port"

    def closeSerial( self ):
        try: 
            if self.serialPort:
                self.serialPort.flush()
                self.serialPort.close()
        finally:
            self.serialPort = None
            return

    def getSerialPort( self ):
        #try to connect to EBB devices
        for strComPort in eggbot_scanlinux.findEiBotBoards():
            serialPort = self.testSerialPort( strComPort )
            if serialPort:
                self.actualSerialPort = strComPort
                return serialPort
        
        #if that fails, try any likely ports
        for strComPort in eggbot_scanlinux.findPorts():
            serialPort = self.testSerialPort( strComPort )
            if serialPort:
                self.actualSerialPort = strComPort
                return serialPort

    def testSerialPort( self, strComPort ):
        '''
        Return a SerialPort object for port with EBB
        NOTE: need to close this serial port
        '''
        try:
            serialPort = pyserial.Serial( strComPort, timeout = 1 )
        
            serialPort.setRTS()
            serialPort.setDTR()
            serialPort.flushInput()
            serialPort.flushOutput()

            time.sleep( 0.1 ) 
        
            serialPort.write( 'v\r' )
            strVersion = serialPort.readline()

            if strVersion and strVersion.startswith( 'EBB' ):
                return serialPort
            serialPort.close()
        
        except pyserial.SerialException:
            pass

        return None

    def doCommand(self, cmd):
        try:
            self.serialPort.write( cmd ) 
            response = self.serialPort.readlines()
            for line in response:
                print line
        except:
            print "fail"
            pass



    def disableMotors(self):
        self.doCommand('EM,0,0\r')
    
    def enableMotors(self):
        self.doCommand('EM,1,1\r')
        
    def stepM(self, duration, x, y):
        self.enableMotors()
        self.doCommand('SM,%d,%d,%d\r' %(duration, x, y))
        self.disableMotors()
