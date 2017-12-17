#!/usr/bin/python3

from gpiozero import Button
from time import sleep,time
#from time import sleep,time,localtime,strftime,time
from signal import pause
import subprocess
#from datetime import datetime

holdTime1 = 1
holdTime2 = 3
doubleClickTimeMax = .5
lastClickTime=time()
button = Button (5,pull_up=True,bounce_time=.01,hold_time=1)

def actionCheckPush(aButton):
     global lastClickTime
     clickTime=time()
     trackHold1=True
     trackHold2=True
     reachedHold1=False
     reachedHold2=False
     #strftime("%a, %d %b %Y %H:%M:%S +0000", time())
     print(str(clickTime) + ": button {} pushed".format(aButton)) 
     while (aButton.is_active):
        if(trackHold1 and (time()-clickTime > holdTime1)):
          #print(str(time()) + ": button {} pushed reached hold1".format(aButton))
          trackHold1 = False
          reachedHold1=True
        if(trackHold2 and (time()-clickTime > holdTime2)):
          #print(str(time()) + ": button {} pushed reached hold2".format(aButton)) 
          print("Hold 2 action")
          #https://docs.python.org/3/library/subprocess.html
          subprocess.Popen(["/usr/local/bin/tplinkcmd.pl", "--cmd", 'set_bulb_state', '--state', '0', '-ip', '192.168.8.196'])
          trackHold2 = False
          reachedHold2=True
     if (reachedHold1 and not reachedHold2):
         print("Hold 1 action")
         #print("hold1 turning on light")
         subprocess.Popen(["/usr/local/bin/tplinkcmd.pl", "--cmd", 'set_bulb_state', '--state', '1', '-ip', '192.168.8.196'])
     if (not (reachedHold1 or reachedHold2)):
         #Single or double click. Wait to find out
         while (time()-clickTime<=doubleClickTimeMax):
             if(aButton.is_active):
                #This is a double click
                print("Double click action")
                return
         print("Single click action")

     #print(str(time()) + ": button {} pushed-releaed".format(aButton)) 

def actionCheckRelease(aButton):
     print(str(time()) + ": button {} released".format(aButton)) 

def actionCheckHold(aButton):
     print(str(time()) + ": button {} held".format(aButton)) 

#button.when_released = actionCheckRelease
#button.when_held = actionCheckHold
button.when_pressed = actionCheckPush
print ("ready\n")
pause()
