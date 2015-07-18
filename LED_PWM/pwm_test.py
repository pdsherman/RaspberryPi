from __future__ import print_function
from random import randrange
import rgb_led, os, time

def showDisplay(option):
   os.system('clear') 
   prompt = 0 
   returnVal = 0

   #List of strings that join together to create display for user
   lines = []
   lines.append('-'*15 + 'LED Strip Demo' + '-'*14 + '\n')
   lines.append('|' + ' '*5 + 'Red:' + ' '*4 + '|' + ' '*3 + 'Green:' + ' '*4 + '|'+ ' '*4 + 'Blue:'+' '*4 + '|\n')
   lines.append('|' + ' '*5 + '%3d' % colors[0] + ' '*5)
   lines.append('|' + ' '*5 + '%3d' % colors[1] + ' '*5)
   lines.append('|' + ' '*5 + '%3d' % colors[2] + ' '*5 + '|\n')
   lines.append('-'*43 + '\n')
   lines.append('|' + ' '*14 + 'RGB Hex Code:' + ' '*14 + '|\n')
   lines.append('|' + ' '*18 + '0x%06X'%rgbVal + ' '*15 + '|\n') 
   lines.append('-'*43 + '\n')
   lines.append('|' + ' '*12 + 'Flash Rate (bpm):' + ' '*12 + '|\n')
   lines.append('|' + ' '*19 + '%3d' % flashRate + ' '*19 + '|\n') 
   lines.append('-'*43 + '\n')

   if option == 0:
      lines.append('|  1. Set red' + ' '*29 + '|\n')
      lines.append('|  2. Set green' + ' '*27 + '|\n')
      lines.append('|  3. Set blue' + ' '*28 + '|\n')
      lines.append('|  4. Set RGB color' + ' '*23 + '|\n')
      lines.append('|  5. Show all PreSet Colors' + ' '*14 + '|\n')
      lines.append('|  6. Set Flash Rate' + ' '*22 + '|\n')
      lines.append('|  7. Exit' + ' '*32 + '|\n')
      prompt = '  Select Option: '
   elif option in [1, 2, 3]:
      strColors = ['Red', 'Green', 'Blue']
      lines.append(('|' + ' '*41 + '|\n')*2)
      lines.append('|' + ' '*6 + 'Set Value (0-255) for: %-5s' % strColors[option-1] + ' '*7 + '|\n')
      lines.append(('|' + ' '*41 + '|\n')*3)
      prompt = '   Value: ' 
   elif option == 4:
      lines.append(('|' + ' '*41 + '|\n')*2)
      lines.append('|' + ' '*8 + 'Set Value for RGB Color.' + ' '*9 + '|\n')
      lines.append('|' + ' '*6 + 'Prefix "0x" to input for hex' + ' '*7 + '|\n')
      lines.append(('|' + ' '*41 + '|\n')*2)
      prompt = '   Value: '
   elif option == 5:
      lines.append(('|' + ' '*41 + '|\n')*2)
      lines.append('|' + ' '*2 + 'Waiting for Color Change to Finish...' + ' '*2 + '|\n')
      lines.append(('|' + ' '*41 + '|\n')*3)
   elif option == 6:
      lines.append(('|' + ' '*41 + '|\n')*2)
      lines.append('|' + ' '*4 + 'Set Flash Rate (Beat per Minute)'+ ' '*5 + '|\n')
      lines.append('|' + ' '*10 + 'Enter 0 for always on'+ ' '*10 + '|\n')
      lines.append(('|' + ' '*41 + '|\n')*1)
      prompt = '   New BPM: '
   lines.append('-'*43 + '\n')

   #Create one long string to display on console
   display = ''.join(lines)
   print(display, end='')
  
   if prompt:
      #Ignore if user input isn't valid integer
      try:
         returnVal = int(input(prompt))
      except NameError:
         returnval = 0


   return returnVal
   
def menu():
   global rgbVal, colors, flashRate

   while True:
      reply = showDisplay(0)

      if reply in (1, 2, 3): #Set individual color
         tempVals = list(colors)
         tempVals[reply - 1] = showDisplay(reply)
         newrgbVal = rgb_led.setColors(tempVals[0], tempVals[1], tempVals[2])
      elif reply == 4: #Set RGB color code
         newVal = showDisplay(reply)
         newrgbVal = rgb_led.setRGB(newVal)
      elif reply == 5: #Fade to random color
         showDisplay(reply)
         #newrgbVal = rgb_led.fadeToNewColor(randrange(256), randrange(256), randrange(256))
         for i in range(16):
            rgb_led.usePreSetColor(i)
            time.sleep(0.75)
         newrgbVal = rgb_led.setRGB(0)
      elif reply == 6: #Changing Flashing Rate of LEDs
         flashRate = showDisplay(reply)
         rgb_led.setBPM(flashRate)
         continue
      elif reply == 7: #Exit Program 
         os.system('clear')
         break
      else: #Show main menu
         continue

      #Update Saved RGB value and color values
      if newrgbVal != -1:
            rgbVal = newrgbVal
            colors = [rgbVal>>16, (rgbVal>>8)&0xFF, rgbVal&0xFF]

# main code
colors = [0, 0, 0]
rgbVal = 0
flashRate = 60
rgb_led.init_PWM(initDutyCycle = [0]*3, flashRate=60)
menu()
