#requires package "PYserial" to be installed NOT package "serial"
#test for this on Windows using "pip list|findstr serial" to ensure that you see PYserial and not serial.
import time,serial
import inspect
from time import sleep

#A class representing one universe of dmx controllers accessed by a serial port.
#Initialising the class opens the port if it can. If not it passes on the IOError exception.
#the first argument of the exception is the name of the port supplied.
#Requires Python 3.6 and above.
class DmxUniverse:
  def __init__(self, serialPort):
    try:
      # Using module serial from package PySerial the following will open the serial port with the given parameters.
      # The baudrate, bytesize, stop bits and parity are the standard dmx requirements.
      # in PYserial initialising serial opens the port automatically if one is given.
      self.serial = serial.Serial(serialPort, baudrate=250000, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_TWO, 
      parity=serial.PARITY_NONE)
      self.dmxData = bytearray(513) #This is the standard message [0] being zero, the rest the levels, one byte/channel
      #Python guarantees it starts off zero but remember that the fixtures may be already se to something else.
    except OSError as e:
    	print("exception=",inspect.getmembers(e))
    	print("OS error: {0}".format(e))
    	raise OSError(serialPort,e)

  # the channels are 1 to 512. Intensity always to 0 to 255.
  #The first byte of the packet for controlling lights is always sent as zero.
  def setChannel(self, chan, intensity):    
    self.dmxData[max(1, min(chan, 512))] = max(0, min(intensity, 255))
    
  def blackout(self):
    for i in range(1, 512, 1):
      self.dmxData[i] = 0

  def makeithappen(self):
  	self.serial.send_break(0.0001) #start of packet must be > 88 microseconds low
  	sleep(0.0001) #then the line has to go high again >8 microseconds
  	self.serial.write(self.dmxData) #send out the entire packet.
#to print it, uncomment below
#  	for k in range(513):
#  	  print(format(self.dmxData[k],'02x'),end='')
# 	print('\n')
  
print('hello')
port='COM'
try:
  dmx = DmxUniverse(port)
except OSError as inst:
  print('Problem opening serial "',inst.args[0],'"')
  print(inst.args[1].args[0])
  print('for Windows 10 must be of form "COMx" where x is number')
  exit()
time.sleep(1)
dmx.blackout() #note, the class above does not clear all the fixtures to zero. Do this to make it happen.
dmx.makeithappen()
time.sleep(1)

for x in range(4):
  realcount=x+1
  dmx.setChannel(realcount,255)
  dmx.makeithappen()
  print('sent ',realcount)
  time.sleep(0.5)
time.sleep(1)
print('going down now')
for x in range(4):
  realcount=x+1
  dmx.setChannel(realcount,128)
  dmx.makeithappen()
  print('sent ',realcount)
  time.sleep(0.5)
time.sleep(1)

print('even lower')
for x in range(4):
  realcount=x+1
  dmx.setChannel(realcount,64)
  dmx.makeithappen()
  print('sent ',realcount)
  time.sleep(0.5)

print('and zero')
for x in range(4):
  realcount=x+1
  dmx.setChannel(realcount,0)
  dmx.makeithappen()
  time.sleep(0.5)

time.sleep(1)

print('bye')