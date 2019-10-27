#requires package "PYserial" to be installed NOT package "serial"
#test for this on Windows using "pip list|findstr serial" to ensure that you see PYserial and not serial.
#edit the line beginning "port=" to correspond with your serial line port accessing the DMS universe.
import time,serial
import inspect
from time import sleep
port='COM3'
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
      self.dmxData = bytearray(513) #This is the standard dmx message, [0] being zero, the rest the levels, one byte/channel
      #Python guarantees it starts off zero but remember that the fixtures may be already set to something else.
    except OSError as e:
#inspect.getmembers returns all the members of an object in a list of (name, value) pairs sorted by name
#    	print("exception=",inspect.getmembers(e))
#    	print("OS error: {0}".format(e))
#Although I fed the port label out with this error, no real need since it is in the string arg of the exception instance.
    	raise OSError(serialPort,e)

  # the channels are 1 to 512. Intensity always to 0 to 255.
  #The first byte of the packet for controlling lights is always sent as zero.
  #the class remembers the settings for each channel so, for example, to dim one light only requires one channel to be updated.
  #Calling "makeithappen" will update ALL the channels with the latest of every previous value set.
  def setChannel(self, chan, intensity):    
    self.dmxData[max(1, min(chan, 512))] = max(0, min(intensity, 255))
    
  def blackout(self):
    for i in range(1, 512, 1):
      self.dmxData[i] = 0

  def makeithappen(self):
  	self.serial.send_break(0.0001) #start of packet must be > 88 microseconds low
  	#the above blocks until the required elapsed time has passed.
  	#after the break, the line will resume its normal high state.
  	sleep(0.0001) #then the line has to stay high again >8 microseconds
  	#the values above are very generous, but the dmx spec does not give an upper limit.
  	self.serial.write(self.dmxData) #send out the entire packet.
#to print it, uncomment below
#  	for k in range(513):
#  	  print(format(self.dmxData[k],'02x'),end='')
# 	print('\n')
  
print('hello')
try:
  dmx = DmxUniverse(port)
except OSError as inst:
	#I had a lot of problems trying to decode what Pyserial does with exceptions.
	#The documentation claims that the exception serial.serialutil.SerialException
  print('Problem opening serial "',inst.args[0],'"')
#The line below was a source of problems to me. I was under the impression that the exception class had attribute errno (and others)
#indeed it does, but that, and all other expected attributes are empty except one called "args" (aaarrrggghhh) which
#contains a complex string typically reading:
#"could not open port 'COM': FileNotFoundError(2, 'The system cannot find the file specified.', None, 2)"
#i.e. pyserial has abandoned the principle of giving error numbers and explanations separately it would seem.
  print(inst.args[1].args[0])
  print('for Windows 10 must be of form "COMx" where x is number')
  exit()
time.sleep(1)
dmx.blackout() #note, the class above does not clear all the fixtures to zero. Do this to set all fixtures to zero.
dmx.makeithappen() #then make it happen
time.sleep(1)

#set the first 4 channels to high, then medium, then low then off, just to show it can be done.
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