import sys
import Adafruit_DHT
import time
import datetime 
from datetime import timedelta
import MySQLdb
from Subfact_ina219 import INA219
import RPi.GPIO as GPIO
from threading import Thread

GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

ina = INA219(address=int('0x40',16))

#GPIO.output(16,0)
#GPIO.output(13,0)


pwm = GPIO.PWM(13,80)
pwm.start(0)

pwm2 = GPIO.PWM(16,80)
pwm2.start(0)

pwm3 = GPIO.PWM(18,80)
pwm3.start(0)

def powerConsuption():
    while True:
   
        
        dba = MySQLdb.connect("localhost","root","password","energy")
        cursor = dba.cursor()
    
        humidity, temperature = Adafruit_DHT.read_retry(11, 4) 
        busVoltage = ina.getBusVoltage_V()
    
        temp = 0

        #for loop to get average of the current from 100 samples.
        for x in range(0,19):
            temp += ina.getCurrent_mA()
        current = temp/20
        power = busVoltage * current/1000
        kwh = 0.000000277 * power
        wh = pow(2.77777777778,-4) * power
        #print "no siema"    
        try:
            cursor.execute("UPDATE power SET volt=%s, current=%s, watt=%s, kwh=%s, wh=%s, humidity=%s, temperature=%s, on_light=%s, off_light=%s WHERE ID = 1", (busVoltage, current, power, kwh, wh, humidity, temperature, lightOn, lightOff))
            dba.commit()
        except MySQLdb.Error, e:
            print e
        cursor.close()
        del cursor
        dba.close()
    #time.sleep(0.2)

#set thread constructor. target to powerConsuption. this function send energy usage on seperate thread
t1 = Thread(target = powerConsuption)

#start thread
t1.start()

#function to update database status and brightnes when timer time elapse or when timer is started
def sendStatus(light, status):
    
    #"UPDATE status SET $light = '$status' WHERE ID = '1'"
    #sql = "UPDATE status SET light_" + lightToString + " = " + status + " WHERE ID = 1"
    sqlStatus = "UPDATE status SET light_" + str(light) + " = " + status + " WHERE ID = 1"
    sqlBright = "UPDATE brightness SET light_" + str(light) + " = " + status + " WHERE ID = 1"
    dba = MySQLdb.connect("localhost","root","password","light_control")
    cursor = dba.cursor()
    try:
        cursor.execute(sqlStatus)
        dba.commit()
        if status == '0':
            cursor.execute(sqlBright)
            dba.commit()
    except MySQLdb.Error, e:
        print e
    cursor.close()
    del cursor
    dba.close()

#reset timer in database when time elapsed
def resetTimer(light):

    #"UPDATE status SET $light = '$status' WHERE ID = '1'"
    #sql = "UPDATE status SET light_" + lightToString + " = " + status + " WHERE ID = 1"
    sqlTimeFrom = "UPDATE time_from SET light_" + str(light) + " = 0 WHERE ID = 1"
    sqlTimeUntil = "UPDATE time_until SET light_" + str(light) + " = 0 WHERE ID = 1"
    dba = MySQLdb.connect("localhost","root","password","light_control")
    cursor = dba.cursor()
    try:
        cursor.execute(sqlTimeFrom)
        dba.commit()
        cursor.execute(sqlTimeUntil)
        dba.commit()
    except MySQLdb.Error, e:
        print e
    cursor.close()
    del cursor
    dba.close()


######BUG IN THE FUNCTION NEED TO BE FIXED!############TIMESTAMP ISSUE CAN'T CONVERT IF NULL IS PASSED!!#####
def controlLight(lightBrightness, lightStatus, timeFrom, timeUntil, lightTurnOn):
    if lightTurnOn == 1:
    
        if int(lightStatus) == 1 or int(lightBrightness) > 0 or timeFrom != '0' or timeUntil != '0':
            #if timer is selected on the andriod app
            if timeFrom != '0' or timeUntil != '0':
                
                if timeFrom == '0':
                    timeFromUnix = 0
                else:    
                    timeFromUnix = int(time.mktime(time.strptime(timeFrom, '%Y/%m/%d %H:%M:%S' )))
                if timeUntil == '0':
                    timeUntilUnix = 0
                else:    
                    timeUntilUnix = int(time.mktime(time.strptime(timeUntil, '%Y/%m/%d %H:%M:%S' )))
               
                #dtime = datetime.datetime.now() 
                dtime = datetime.datetime.now() + timedelta(hours=1)
                print dtime 
                currentTimeUnix = time.mktime(dtime.timetuple())
                
                if currentTimeUnix >= timeFromUnix and int(lightBrightness) > 0:
                    sendStatus(lightTurnOn, '1')  
                    pwm.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm.ChangeDutyCycle(0)
            
            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm.ChangeDutyCycle(int(lightBrightness))

        else: 
            pwm.ChangeDutyCycle(0)

    elif lightTurnOn == 2:

        if int(lightStatus) == 1 or int(lightBrightness) > 0 or timeFrom != '0' or timeUntil != '0':
            #if timer is selected on the andriod app
            if timeFrom != '0' or timeUntil != '0':

                if timeFrom == '0':
                    timeFromUnix = 0
                else:
                    timeFromUnix = int(time.mktime(time.strptime(timeFrom, '%Y/%m/%d %H:%M:%S' )))
                if timeUntil == '0':
                    timeUntilUnix = 0
                else:
                    timeUntilUnix = int(time.mktime(time.strptime(timeUntil, '%Y/%m/%d %H:%M:%S' )))

                dtime = datetime.datetime.now()
                currentTimeUnix = time.mktime(dtime.timetuple())

                if currentTimeUnix >= timeFromUnix:

                    if int(lightBrightness) < 1:
                        lightBrightness = 100
                    pwm2.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0':
                    pwm2.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):

                if int(lightBrightness) < 1:
                    lightBrightness = 100
                pwm2.ChangeDutyCycle(int(lightBrightness))

            #if int(lightStatus) == 0 and int(lightBrightness) == 0 and int(timeFrom) == 0 and int(timeUntil) == 0:
                #pwm.ChangeDutyCycle(0)

        else:
            pwm2.ChangeDutyCycle(0)

    elif lightTurnOn == 3:

        if int(lightStatus) == 1 or int(lightBrightness) > 0 or timeFrom != '0' or timeUntil != '0':
            #if timer is selected on the andriod app
            if timeFrom != '0' or timeUntil != '0':

                if timeFrom == '0':
                    timeFromUnix = 0
                else:
                    timeFromUnix = int(time.mktime(time.strptime(timeFrom, '%Y/%m/%d %H:%M:%S' )))
                if timeUntil == '0':
                    timeUntilUnix = 0
                else:
                    timeUntilUnix = int(time.mktime(time.strptime(timeUntil, '%Y/%m/%d %H:%M:%S' )))

                dtime = datetime.datetime.now()
                currentTimeUnix = time.mktime(dtime.timetuple())

                if currentTimeUnix >= timeFromUnix:

                    if int(lightBrightness) < 1:
                        lightBrightness = 100
                    pwm3.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0':
                    pwm3.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):

                if int(lightBrightness) < 1:
                    lightBrightness = 100
                pwm3.ChangeDutyCycle(int(lightBrightness))

            #if int(lightStatus) == 0 and int(lightBrightness) == 0 and int(timeFrom) == 0 and int(timeUntil) == 0:
                #pwm.ChangeDutyCycle(0)

        else:
            pwm3.ChangeDutyCycle(0)
        

while True:

    #t1.start()

    db = MySQLdb.connect("localhost","root","password","light_control")

    cursor = db.cursor()

    sqlBright = "SELECT * FROM brightness where ID = '%d'" %(1)
    sqlStatus = "SELECT * FROM status where ID = '%d'" %(1)
    sqlFrom = "SELECT * FROM time_from where ID = '%d'" %(1)
    sqlUntil = "SELECT * FROM time_until where ID = '%d'" %(1)
    
    
    #humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #busVoltage = ina.getBusVoltage_V()
    #current = ina.getCurrent_mA()
    #power = busVoltage * current/1000
    #kwh = 0.000000277 * power
    #wh = pow(2.77777777778,-4) * power
   
    try:
        #cursor.execute("UPDATE power SET volt=%s, current=%s, watt=%s, kwh=%s, wh=%s WHERE ID = 1", (busVoltage, current, power, kwh, wh))
        #db.commit()

        lightOn = 0
        lightOff = 0

        cursor.execute(sqlBright)
        results = cursor.fetchall()
        for brightness in results:   
            bright1 = brightness[1]
            bright2 = brightness[2]
            bright3 = brightness[3]
            #bright.append(brightness[1])
            #bright.append(brightness[2])
            #bright.append(brightness[3])
            #print "BRIGHTNESS1 = %s,BRIGHTNESS2 = %s, BRIGHTNESS3 = %s" % (bright1, bright2, bright3 )


        cursor.execute(sqlStatus)
        results = cursor.fetchall()
        for lightStatus in results:
            status1 = lightStatus[1]
            status2 = lightStatus[2]
            status3 = lightStatus[3]
            #print "STATUS1 = %s,STATUS2 = %s, STATUS3 = %s" % (status1, status2, status3 )

        cursor.execute(sqlFrom)
        results = cursor.fetchall()
        for timeFrom in results:
            from1 = timeFrom[1]
            from2 = timeFrom[2]
            from3 = timeFrom[3]
            #print "timeFrom1 = %s timeFrom = %s, timeFrom3 = %s" % (from1, from2, from3 )


        cursor.execute(sqlUntil)
        results = cursor.fetchall()
        for until in results:
            until1 = until[1]
            until2 = until[2]
            until3 = until[3]
            #print "timeUntil1 = %s timeUntil2 = %s, timeUntil3 = %s" % (until1, until2, until3 )
          
        for x in range(1,4):
            controlLight(brightness[x], lightStatus[x], timeFrom[x], until[x], x)
            #powerConsuption()
            #print "eniu co tam"
            #print brightness[x]
        #powerConsuption()
        #print "siema ---> "
        #print brightness[1]

        #print " "

    except MySQLdb.Error, e:
        print e


    cursor.close()
    del cursor
    db.close()

    #time.sleep(1);    
    #print " "
    #print " "
