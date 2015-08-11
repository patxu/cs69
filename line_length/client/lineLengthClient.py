#!/usr/bin/python

#code partially taken from web source:
#http://www.bytecreation.com/blog/2013/10/13/raspberry-pi-ultrasonic-sensor-hc-sr04

import sys

from http.client import *
from socket import error as socket_error
import errno

import time
import RPi.GPIO as GPIO

#GPIO pin values
ECHOPIN = 17
TRIGPIN = 18

#set up GPIO pins and server connection; make inital "start" request
def setup():
  # values of the GPIO pins, not the physical location
  GPIO.setmode(GPIO.BCM)

  # GPIO output = the pin that's connected to "Trig" on the sensor
  # GPIO input = the pin that's connected to "Echo" on the sensor
  GPIO.setup(TRIGPIN,GPIO.OUT)
  GPIO.setup(ECHOPIN,GPIO.IN)
  GPIO.output(TRIGPIN, GPIO.LOW)

  address, port = get_arguments()
  connection = HTTPConnection(address, port)
  makeGetRequest(connection, "start") #send special start request
  while True:
    units = input("Choose your distance units (cm/ft): ")
    if units == "ft" or units == "cm":
      makeGetRequest(connection, units) #send special start request
      print("Starting distance measurements!\n")
      break
    else:
      print("Input not recognized! Try again.")
  return connection

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

def cleanup():
  GPIO.cleanup()             # Release resource

#get a sensor reading
def getReading():
  # found that the sensor can crash if there isn't a delay here
  # no idea why. If you have odd crashing issues, increase delay
  time.sleep(1)

  # sensor manual says a pulse length of 10Us will trigger the 
  # sensor to transmit 8 cycles of ultrasonic burst at 40kHz and 
  # wait for the reflected ultrasonic burst to be received

  # pulse length of 10 micro seconds (0.00001 seconds)
  GPIO.output(TRIGPIN, True)
  time.sleep(0.00001)
  GPIO.output(TRIGPIN, False)

  # 0 means nothing is happening
  while GPIO.input(ECHOPIN) == 0:
    signaloff = time.time()

  # 1 means a signal is received
  while GPIO.input(ECHOPIN) == 1:
    signalon = time.time()

  timepassed = signalon - signaloff
  distance = timepassed * 17150

  return distance

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
    cleanup()
    exit(1)

if __name__ == '__main__':     # Program start from here

  connection = setup()
  try:
    while 1:
      makeGetRequest(connection, str(getReading()))
      time.sleep(1)
  except KeyboardInterrupt:
    cleanup()

