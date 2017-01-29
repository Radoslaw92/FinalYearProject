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

#def controlLight(lightBrightness, lightStatus, timeFrom, timeUntil, lightTurnOn):
#    if lightStatus == 1:
#        if lightTurnOn == 1:
#            GPIO.output(13, 0)
#        elif lightTurnOn == 2:
#            GPIO.output(16, 0)
#        elif lightTurnOn == 2:
#            GPIO.output(18, 0)
#        print "light status =="
#        print lightStatus


GPIO.output(16,0)
GPIO.output(13,0)


pwm = GPIO.PWM(13,80)
pwm.start(0)

pwm2 = GPIO.PWM(16,80)
pwm2.start(0)

pwm3 = GPIO.PWM(18,80)
pwm3.start(0)



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
               
                dtime = datetime.datetime.now() 
                currentTimeUnix = time.mktime(dtime.timetuple())
                
                if currentTimeUnix >= timeFromUnix:
    
                    if int(lightBrightness) < 1:
                        lightBrightness = 100  
                    pwm.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0':
                    pwm.ChangeDutyCycle(0)
            
            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
               
                if int(lightBrightness) < 1:
                    lightBrightness = 100
                pwm.ChangeDutyCycle(int(lightBrightness))

            #if int(lightStatus) == 0 and int(lightBrightness) == 0 and int(timeFrom) == 0 and int(timeUntil) == 0:
                #pwm.ChangeDutyCycle(0)

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

    db = MySQLdb.connect("localhost","root","password","light_control")

    cursor = db.cursor()

    sqlBright = "SELECT * FROM brightness where ID = '%d'" %(1)
    sqlStatus = "SELECT * FROM status where ID = '%d'" %(1)
    sqlFrom = "SELECT * FROM time_from where ID = '%d'" %(1)
    sqlUntil = "SELECT * FROM time_until where ID = '%d'" %(1)
 

    try:
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
            #print "eniu co tam"
            #print brightness[x]
        #print "siema ---> "
        #print brightness[1]

        #print " "

    except:
        print "Cant get data from DataBase"

    #time.sleep(0.2);    
    #print " "
    #print " "
