"""
    File: rgb_led.py
  Author: P. Sherman 
    Date: 15 July 2015
 
   Description:
     Module to control the flashing and color
     of RGB LED strips.
"""

#----------- Imports --------------
from __future__ import print_function
import time, wiringpi2

#-------- Module Variables ---------
preSetColors = []

#-------- Module Functions ---------
"""
Function: init_PWM
-----------------------
Description:
  Uses wiringPi library to setup 3 pins on Raspberry Pi
  for PWM outputs to control lighting of RGB LED strip.
Param:
   redPin, greenPin, bluePin - Physical pin num on Raspberry Pi with PWM output
   initDutyCycle  - intital duty cycle of PWM signals 
Return:
   0  - successful initialization of pwm signals
   -1 - error during set up 
"""
def init_PWM(_redPin = 23, _greenPin = 24, _bluePin = 25, _flashPin= 22, initDutyCycle = [100]*3, flashRate = 0): 
   global colorPins, colors, flashActive, flashPin 
 
   colorPins = [_redPin, _greenPin, _bluePin] #list for pins used in raspberry pi

   wiringpi2.wiringPiSetup() # Initialize using wiringPi pin numbering scheme   

   for dc in initDutyCycle: #Check for valid initial duty cycle
      if dc < 0 or dc > 255: return -1

   #Create intial PWM signals for input to LED strip
   for i in range(3):
      wiringpi2.softPwmCreate(colorPins[i], int(initDutyCycle[i]*100.0/255.0), 100)

   #Current RGB values of LED strip
   colors = list(initDutyCycle)

   #Create square wave for flashing beat
   flashPin = _flashPin
   wiringpi2.softToneCreate(flashPin)
   if flashRate != 0:
      wiringpi2.softToneWrite(flashPin, flashRate)
      flashActive = True
   else:
      wiringpi2.softToneStop(flashPin)
      flashActive = False

   #Use Colors.txt file to create list of preset color options
   readColorsFile()

   return 0
"""
Function: readColorsFile
-----------------------
Description:
   Reads Text File of numbers to make list of pre-set colors
Param:
   None
Return:
   None
"""
def readColorsFile():
   global preSetColors

   #Open file and read first line to ignore
   colorFile = open("colors.txt")
   line_to_ignore = colorFile.readline() #Red,Green,Blue
  
   lineList = colorFile.readlines()
   #Read File colors.txt
   for line in lineList:
      parts = line.split(',')
      preSetColors.append( [int(num) for num in parts] )

"""
Function: setColors
-----------------------
Description:
   Set RGB values of LED strip using duty cycle of PWM signals
Param:
   red, green, blue  -  values between (0-256) to set RGB colors of LED
Return:
   RGB value - defined as (R*65536)+(G*256)+B
                  ... or ...
       -1    - Error: input value outside of 0-255
"""
def setColors(red, green, blue):
   global colors

   #Check if inputs are in valid range 
   for c in (red, green, blue): 
      if c < 0 or c > 255: return -1

   colors = [red, green, blue] 

   for (clr, pin) in zip(colors, colorPins):
         wiringpi2.softPwmWrite(pin, int(clr*100.0/255.0))

   return (red*65536 + green*256 + blue)

"""
Function: usePreSetColor
-----------------------
Description:
Param:
Return:
"""
def usePreSetColor(index):
   if index > 0 and index < len(preSetColors):
      setColors(preSetColors[index][0], preSetColors[index][1], preSetColors[index][2])

"""
Function: setRGB
-----------------------
Description:
   Sets RGB values of LED based on singe value with 
   RGB = (Red*65536) + (Green*256) + Blue
Param:
   rgb  - RGB color code as defined in function description 
Return:
   -1 if invalid rgb value or other error / rgb input otherwise
"""
def setRGB(rgb):
   red = rgb >> 16;
   green = (rgb >> 8) & 0xFF
   blue = rgb & 0xFF

   if rgb == setColors(red, green, blue):
      return rgb

   return -1

"""
Function: fadeToNewColor
-----------------------
Description:
   Slowly changes LED strip to new color 
Param:
   newRed, newGreen, newBlue  -  target values for new RGB values   
   maxStep  -  maximum increment during color change process
   timeStep -  time (in seconds) that process delays for each increment towards new color
Return:
   -1 if some error / 0 otherwise
"""
def fadeToNewColor(newRed, newGreen, newBlue, maxStep = 10, timeStep = 0.2):
   global colors
   
   #Check if new colors are valid 
   for c in (newRed, newGreen, newBlue):
      if c < 0 or c > 255: return -1

   """
   Loop until LED colors match the target input colors.
   for each iteration, the difference between individual
   colors are found and the LED colors are moved towards
   the target with a maximum step set by function input
   """ 
   targetColors = [newRed, newGreen, newBlue]
   newRgbVal = 0

   while(targetColors != colors): 
      tempColor = list(colors)
      for i in range(3):
         diff = targetColors[i] - colors[i]
         if diff > 0:
            step = diff if diff < maxStep else maxStep
         else:
            step = diff if diff > -maxStep else -maxStep
         tempColor[i] += step
      newRgbVal = setColors(tempColor[0], tempColor[1], tempColor[2]) 
      if newRgbVal == -1: 
         return -1 
      
      time.sleep(timeStep)

   return newRgbVal

"""
Function: setBPM
-----------------------
Description:
   Set flash rate of LEDs 
Param:
   flashRate - Rate in (Beats per minute) to set flash rate of LED strip. Zero for always on.
Return:
"""
def setBPM(flashRate):
   global flashActive

   if flashRate != 0:
      if not flashActive:
         wiringpi2.softToneCreate(flashPin)
         flashActive = True
      wiringpi2.softToneWrite(flashPin, flashRate)

   else:
      if flashActive:
         wiringpi2.softToneStop(flashPin)
         flashActive = False

"""
  Code for Debugging
"""
if __name__ == '__main__':
   init_PWM()
   for i in range(16):
      usePreSetColor(i)
      time.sleep(0.5)

   setBPM(140)
   for i in range(16):
      usePreSetColor(i)
      time.sleep(0.5)

   setRGB(0)

