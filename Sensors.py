#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import datetime 


while True:

    now = time.strftime("%c")
    dtime = datetime.datetime.now()
    timestamp = time.mktime(dtime.timetuple())
    currentTime = ("Current time is %s" % now)

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    time.sleep(1)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} % '.format(temperature, humidity) + currentTime 
    print  " Unix time is: " + str(timestamp)
    #print ("Current time is %s" % now)

