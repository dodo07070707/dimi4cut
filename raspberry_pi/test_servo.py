import RPi.GPIO as g
import time

servoPin = 12
duty = (5,7.5,10,7.5)
idx = 0

g.setmode(g.BCM)
g.setup(servoPin,g.OUT)

servo = g.PWM(servoPin, 50)
servo.start(duty[idx])
time.sleep(1)

try:
    while True:
        idx = (idx+1)%4
        servo.ChangeDutyCycle(duty[idx])
        time.sleep(10)

except KeyboardInterrupt:
    servo.ChangeDutyCycle(duty[0])    
    servo.stop()
    g.cleanup()

