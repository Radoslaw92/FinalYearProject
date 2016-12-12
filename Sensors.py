#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import datetime 
from Subfact_ina219 import INA219
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

ina = INA219(address=int('0x40',16))

while True:

    #ina = INA219(address('0x40',16)
    now = time.strftime("%c")
    dtime = datetime.datetime.now()
    timestamp = time.mktime(dtime.timetuple())
    currentTime = ("Current time is %s" % now)

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    time.sleep(1)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} % '.format(temperature, humidity) + currentTime 
    print  " Unix time is: " + str(timestamp)
    #print ("Current time is %s" % now)
    GPIO.output(13, 1)
    GPIO.output(16, 1)
    GPIO.output(18, 1)
    GPIO.output(37, 1)

    busVoltage = ina.getBusVoltage_V()
    current = ina.getCurrent_mA()
    power = busVoltage * current/1000

    print "Bus voltage: %.3f V" % busVoltage
    print "Current: %.3f mA" % current
    print "Current power consuption %.5f Watts" % power

