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

GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

GPIO.setup(36, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

GPIO.setup(31, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

ina = INA219(address=int('0x40',16))

#GPIO.output(16,0)
#GPIO.output(13,0)


pwm = GPIO.PWM(40,80)
pwm.start(0)
pwm2 = GPIO.PWM(38,80)
pwm2.start(0)
pwm3 = GPIO.PWM(37,80)
pwm3.start(0)

pwm4 = GPIO.PWM(36,80)
pwm4.start(0)
pwm5 = GPIO.PWM(35,80)
pwm5.start(0)
pwm6 = GPIO.PWM(33,80)
pwm6.start(0)

pwm7 = GPIO.PWM(31,80)
pwm7.start(0)
pwm8 = GPIO.PWM(29,80)
pwm8.start(0)
pwm9 = GPIO.PWM(26,80)
pwm9.start(0)

pwm10 = GPIO.PWM(24,80)
pwm10.start(0)
pwm11 = GPIO.PWM(23,80)
pwm11.start(0)
pwm12 = GPIO.PWM(22,80)
pwm12.start(0)
lightOnCount = 0
lightOnValue = 0

def powerConsuption():
    while True:
   
        
        dba = MySQLdb.connect("localhost","root","password","energy")
        cursor = dba.cursor()
    
        humidity, temperature = Adafruit_DHT.read_retry(11, 4) 
        busVoltage = ina.getBusVoltage_V()
    
        temp = 0
        lightOn = lightOnValue
        lightOff = 12 - lightOnValue
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


##controling lights##
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

                #dtime = datetime.datetime.now()
                dtime = datetime.datetime.now() + timedelta(hours=1)
                print dtime
                currentTimeUnix = time.mktime(dtime.timetuple())

                if currentTimeUnix >= timeFromUnix and int(lightBrightness) > 0:
                    sendStatus(lightTurnOn, '1')
                    pwm2.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm2.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm2.ChangeDutyCycle(int(lightBrightness))
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

                #dtime = datetime.datetime.now()
                dtime = datetime.datetime.now() + timedelta(hours=1)
                print dtime
                currentTimeUnix = time.mktime(dtime.timetuple())

                if currentTimeUnix >= timeFromUnix and int(lightBrightness) > 0:
                    sendStatus(lightTurnOn, '1')
                    pwm3.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm3.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm3.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm3.ChangeDutyCycle(0)
       
    elif lightTurnOn == 4:
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
                    pwm4.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm4.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm4.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm4.ChangeDutyCycle(0)

    elif lightTurnOn == 5:
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
                    pwm5.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm5.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm5.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm5.ChangeDutyCycle(0)

    elif lightTurnOn == 6:
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
                    pwm6.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm6.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm6.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm6.ChangeDutyCycle(0)

    elif lightTurnOn == 7:

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
                    pwm7.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm7.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm7.ChangeDutyCycle(int(lightBrightness))

        else:
            pwm7.ChangeDutyCycle(0)

    elif lightTurnOn == 8:
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
                    pwm8.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm8.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm8.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm8.ChangeDutyCycle(0)

    elif lightTurnOn == 9:
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
                    pwm9.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm9.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm9.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm9.ChangeDutyCycle(0)

    elif lightTurnOn == 10:
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
                    pwm10.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm10.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm10.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm10.ChangeDutyCycle(0)

    elif lightTurnOn == 11:
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
                    pwm11.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm11.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm11.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm11.ChangeDutyCycle(0)

    elif lightTurnOn == 12:
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
                    pwm12.ChangeDutyCycle(int(lightBrightness))

                if currentTimeUnix >= timeUntilUnix and timeUntil != '0' and lightBrightness != '0':
                    resetTimer(lightTurnOn)
                    sendStatus(lightTurnOn, '0')
                    pwm12.ChangeDutyCycle(0)

            #if brightness or status is selected on android app
            if (int(lightBrightness) > 0 or int(lightStatus) == 1) and (timeFrom == '0' and timeUntil == '0'):
                pwm12.ChangeDutyCycle(int(lightBrightness))
        else:
             pwm12.ChangeDutyCycle(0)


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
            bright4 = brightness[4]
            bright5 = brightness[5]
            bright6 = brightness[6]
            bright7 = brightness[7]
            bright8 = brightness[8]
            bright9 = brightness[9]
            bright10 = brightness[10]
            bright11 = brightness[11]
            bright12 = brightness[12]

        cursor.execute(sqlStatus)
        results = cursor.fetchall()
        for lightStatus in results:
            status1 = lightStatus[1]
            status2 = lightStatus[2]
            status3 = lightStatus[3]
            status4 = lightStatus[4]
            status5 = lightStatus[5]
            status6 = lightStatus[6]
            status7 = lightStatus[7]
            status8 = lightStatus[8]
            status9 = lightStatus[9]
            status10 = lightStatus[10]
            status11 = lightStatus[11]
            status12 = lightStatus[12]
        
        for i in xrange(len(lightStatus)):
            if lightStatus[i] == '1':
                lightOnCount += 1 
        lightOnValue = lightOnCount
        lightOnCount = 0  

        cursor.execute(sqlFrom)
        results = cursor.fetchall()
        for timeFrom in results:
            from1 = timeFrom[1]
            from2 = timeFrom[2]
            from3 = timeFrom[3]
            from4 = timeFrom[4]
            from5 = timeFrom[5]
            from6 = timeFrom[6]
            from7 = timeFrom[7]
            from8 = timeFrom[8]
            from9 = timeFrom[9]
            from10 = timeFrom[10]
            from11 = timeFrom[11]
            from12 = timeFrom[12]


            #print "timeFrom1 = %s timeFrom = %s, timeFrom3 = %s" % (from1, from2, from3 )


        cursor.execute(sqlUntil)
        results = cursor.fetchall()
        for until in results:
            until1 = until[1]
            until2 = until[2]
            until3 = until[3]
            until4 = until[4]
            until5 = until[5]
            until6 = until[6]
            until7 = until[7]
            until8 = until[8]
            until9 = until[9]
            until10 = until[10]
            until11 = until[11]
            until12 = until[12]

          
        for x in range(1,13):
            controlLight(brightness[x], lightStatus[x], timeFrom[x], until[x], x)
 
    except MySQLdb.Error, e:
        print e


    cursor.close()
    del cursor
    db.close()


