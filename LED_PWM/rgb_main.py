from __future__ import pring_function
from random import randrange
from math import floor
import rgb_led, os, time

#Variables to adjust as needed
posRed   = 0
posGreen = 1
posBlue  = 2
posClr   = 3
posBPM   = 4
posSwt   = 5

mask_manual = 0b01
mask_ClrWhl = 0b10

bpmMax = 230
bpmMin = 30
diffMin = 2
prevBPM_analog = 0

#Intialize Hardware / Variables
rgb_led.init_PWM(initDutyCycle = [0]*3, flashrate = 0)
rgb_led.initSPI(23, 24, 25)


"""
Function: scaleBPM
------------------
Description: takes analog value (0-1024) and scales to 
corresponding beats per minute
"""
def scaleBPM(currBPM_analog):

   diff = abs(currBPM_analog - prevBPM_analog) 
   if(diff > diffMin):
      currBPM = floor( (currBPM_analog / 1024.0) * (bpmMax-bpmMin) + bpmMin )
      prevBPM_analog = currBPM_analog
   else:
      currBPM = floor( (prevBPM_analog / 1024.0) * (bpmMax-bpmMin) + bpmMin )

   if(currBPM_analog < 20):
      currBPM = 0

   return currBPM

"""                      
   Infinite Loop for Project
"""
while(True):
   #Read & Parse Analog Values from PIC
   analogVals = rgb_led.spiGetAnalogVals()
   redVal   = analogVals[posRed]
   greenVal = analogVals[posGreen]
   blueVal  = analogVals[posBlue]
   colorVal = analogVals[posClr]
   bpmVal   = analogVals[posBPM] 
   switches = analogVals[posSwt] 

   #Adjust Beats per Minute
   

   #If: manual control switch on 
   
   #Else if: Color Wheel knob swith on

   #Else: Randomally change color

   
   
