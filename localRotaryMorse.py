#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
 
RoAPin = 11    # pin11
RoBPin = 12    # pin12

morseAlphabet ={
    "A" : ".-",
    "B" : "-...",
    "C" : "-.-.",
    "D" : "-..",
    "E" : ".",
    "F" : "..-.",
    "G" : "--.",
    "H" : "....",
    "I" : "..",
    "J" : ".---",
    "K" : "-.-",
    "L" : ".-..",
    "M" : "--",
    "N" : "-.",
    "O" : "---",
    "P" : ".--.",
    "Q" : "--.-",
    "R" : ".-.",
    "S" : "...",
    "T" : "-",
    "U" : "..-",
    "V" : "...-",
    "W" : ".--",
    "X" : "-..-",
    "Y" : "-.--",
    "Z" : "--..",
    }

inverseMorseAlphabet = dict((v,k) for (k,v) in morseAlphabet.items())
 
globalCounter = 0
 
flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0
 
def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
 
def rotaryDeal():
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global globalCounter
    Last_RoB_Status = GPIO.input(RoBPin)
    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter = globalCounter + 1
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter = globalCounter - 1
 
def loop():
    global globalCounter
    prevGlobalCounter = 0
    lastInputTime = 0

    message = ""
    while True:
      rotaryDeal()
      if (globalCounter != prevGlobalCounter):
        lastInputTime = time.clock()
      if (globalCounter > prevGlobalCounter):
        print "dash"
        message += "-"
      if (globalCounter < prevGlobalCounter):
        print "dot"
        message += "."
      if (globalCounter != prevGlobalCounter):
        prevGlobalCounter = globalCounter
        print lastInputTime
      if (time.clock() - lastInputTime > 1 and lastInputTime != 0):
        print "reset"
        lastInputTime = 0;
        if (message in inverseMorseAlphabet):
          print inverseMorseAlphabet[message]
        else:
          print "Please Try Again"
        message = ""

 
def destroy():
    GPIO.cleanup()             # Release resource
 
if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
