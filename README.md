## DmxUniverse - Interface to dmx serial on Windows.

Being a total python novice I was unable to get https://github.com/trevordavies095/DmxPy.git working on Windows.
I have a qtxlight 4 channel DMX512 dimmer which I wished to use from a script on windows. I purchased an isolated ft232R based driver
for the serial line. This code is based (very loosely) on the code of trevordavies095 but based on a description of the dmx512 original protocol.

This is a crude demonstration of the use of one type of serial interface on Windows 10 to drive a DMX512 4 channel dimmer using Python 3.7.2
It functions with my configuration. It might work with other configurations, I do not know. It is not packaged.
It comes as a simple class to represent  a single DMX Universe and contains  instatiation and invocations of the functions
of that class to demonstrate sending values to the DMX512 equipment.

In total contravention of current industry practice, the code contains comments. Since you will have to modify the code to use it, look there for 
instructions on how to.


