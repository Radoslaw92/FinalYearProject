import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

pwm = GPIO.PWM(37,80)
#pwm2 = GPIO.PWM(16,80)
#pwm3 = GPIO.PWM(13, 80)
pwm.start(0)
#pwm2.start(0)
#pwm3.start(0)
while True:
    print "siema"
    pwm.ChangeDutyCycle(20)
    #pwm2.ChangeDutyCycle(100)
    #pwm3.ChangeDutyCycle(5)
