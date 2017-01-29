#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import datetime
import MySQLdb 
from Subfact_ina219 import INA219
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

ina = INA219(address=int('0x40',16))


while True:
    
    db = MySQLdb.connect("localhost","root","password","light_control")

    cursor = db.cursor()

    sql = "SELECT * FROM brightness where ID = '%d'" %(1)

    try:
        cursor.execute(sql)
        results = cursor.fetchmany()
        for bright in results:
            light1 = bright[1]
            light2 = bright[2]
            light3 = bright[3]
            print "BRIGHTNESS1 = %s,BRIGHTNESS2 = %s, BRIGHTNESS3 = %s" % (light1, light2, light3 )
            light1= null
            light2 = null
            light3 = null
            #cursor.close()

    except:
        print "Cant get data from DataBase"

    result=0
   
    print " no to siema elo %s " % (light2)


    print results
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

