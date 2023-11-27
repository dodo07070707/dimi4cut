import RPi.GPIO as g
import time
import spidev

ledPin = 12

g.setmode(g.BCM)
g.setup(ledPin, g.OUT)

pwm = g.PWM(ledPin, 100)
pwm.start(0)

spi = spidev.SpiDev()
spi.open(0,0) # open No.0 channel
spi.max_speed_hz = 1000000

def ReadVol(vol):
    adc = spi.xfer2([1,(0x08+vol) << 4, 0])
    data = ((adc[1]&0x03) << 8) + adc[2]
    return data

while True:
    a = ReadVol(0)
    pwm.ChangeDutyCycle(a/1023*100)
    time.sleep(0.1)
    
