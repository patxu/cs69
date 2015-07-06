#!/usr/bin/env python

#Some code taken from the Sunfounder Raspberry Pi tutorial.

import sys

from http.client import *
from socket import error as socket_error
import errno

import RPi.GPIO as GPIO
import time
 
RoAPin = 11
RoBPin = 12
 
globalCounter = 0
 
flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0
 
def setup():
  GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
  GPIO.setup(RoAPin, GPIO.IN)    # input mode
  GPIO.setup(RoBPin, GPIO.IN)

def get_arguments():
  arguments = sys.argv
  if len(arguments) != 3:
    error('Usage: python3 client.py <server address> <server port>\nFor example: python3 client.py tahoe.cs.dartmouth.edu 50000')
  address = arguments[1]
  try:
    port = int(arguments[2])
    assert(port >= 1)
  except:
    error("Can't convert {} to a port number ({} should be a positive integer)")
  return address, port

def error(message):
  print(message)
  exit(1)
 
#gets GPIO input from rotary encoder
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
 
#main loop that checks for rotary input
def loop():
  global globalCounter
  prevGlobalCounter = 0 #previous rotary value
  lastInputTime = 0 #last time the user gave input

  address, port = get_arguments()
  connection = HTTPConnection(address, port)
  makeGetRequest(connection, "start") #send special start request

  message = "" #the morse code message e.g. "..-"
  while True:
    rotaryDeal()
    if (globalCounter != prevGlobalCounter):
      lastInputTime = time.clock()
    if (globalCounter > prevGlobalCounter): #counter clockwise = dash
      message += "-"
    if (globalCounter < prevGlobalCounter): #clockwise = dot
      message += "."
    if (globalCounter != prevGlobalCounter):
      prevGlobalCounter = globalCounter
    if (time.clock() - lastInputTime > 1 and lastInputTime != 0): #send this information off to the server
      lastInputTime = 0;
      makeGetRequest(connection, message)
      message = ""

#send a get request to the server
def makeGetRequest(connection, message):
  try:
    connection.request('GET', message)
    response = connection.getresponse()
    print(response.read().decode("utf-8"))
  except socket_error as serr:
    if serr.errno != errno.ECONNREFUSED:
      raise serr
    print("Failed to communicate with server. Is the server code running?")
    exit(1)


def destroy():
  GPIO.cleanup()             # Release resource
 
if __name__ == '__main__':     # Program start from here
  setup()
  try:
    loop()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()
