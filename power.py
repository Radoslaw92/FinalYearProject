#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import datetime
import MySQLdb
from Subfact_ina219 import INA219
import RPi.GPIO as GPIO
from math import expm1 


#GPIO.setmode(GPIO.BOARD)

#GPIO.setup(13, GPIO.OUT)
#GPIO.setup(16, GPIO.OUT)
#GPIO.setup(18, GPIO.OUT)
#GPIO.setup(37, GPIO.OUT)


ina = INA219(address=int('0x40',16))


#GPIO.output(13,1)
#GPIO.output(16,1)
#GPIO.output(18,1)
#GPIO.output(37,1)


while True:

    db = MySQLdb.connect("localhost","root","password","energy")
    cursor = db.cursor()

    #sqlInsert = "UPDATE power SET volt=%d, current=%d, watt=%d, kwh=%d, wh=%d WHERE ID = 1"


    now = time.strftime("%c")
    dtime = datetime.datetime.now()
    timestamp = time.mktime(dtime.timetuple())
    currentTime = ("Current time is %s" % now)

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    #time.sleep(0.2)
    #print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} % '.format(temperature, humidity) + currentTime
    #print  " Unix time is: " + str(timestamp)

    busVoltage = ina.getBusVoltage_V()
    current = ina.getCurrent_mA()
    power = busVoltage * current/1000

    #print "Bus voltage: %.3f V" % busVoltage
    #print "Current: %.3f mA" % current
    #print "Current power consuption %.5f Watts" % power
    kwh = 0.000000277 * power 
    wh = pow(2.77777777778,-4) * power
    #print "the KWh is equal to: "
    #print kwh 
    cursor.execute("UPDATE power SET volt=%s, current=%s, watt=%s, kwh=%s, wh=%s WHERE ID = 1", (busVoltage, current, power, kwh, wh))
    db.commit()
db.close()
