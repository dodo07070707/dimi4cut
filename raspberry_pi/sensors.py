import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import cv2
import numpy as np

# GPIO 설정
button_pin = 17  # 버튼 핀
buzzer_pin = 18  # 부저 핀
segment_pins = [21, 20, 16, 12, 25, 24, 23, 22]  # 7-Segment 핀
led_pin = 26  # LED 핀
potentiometer_pin = 19  # 가변 저항 핀

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(segment_pins, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(potentiometer_pin, GPIO.IN)

pwm = GPIO.PWM(buzzer_pin, GPIO.OUT)
pwm.start(50)

# 7-Segment Display 디지트 맵
digit_map = {
    0: (1, 1, 1, 1, 1, 1, 0),
    1: (0, 1, 1, 0, 0, 0, 0),
    2: (1, 1, 0, 1, 1, 0, 1),
    3: (1, 1, 1, 1, 0, 0, 1),
    4: (0, 1, 1, 0, 0, 1, 1),
    5: (1, 0, 1, 1, 0, 1, 1),
    6: (1, 0, 1, 1, 1, 1, 1),
    7: (1, 1, 1, 0, 0, 0, 0),
    8: (1, 1, 1, 1, 1, 1, 1),
    9: (1, 1, 1, 1, 0, 1, 1),
}

# 카메라 초기화
camera = PiCamera()
camera.start_preview()  # OpenCV로 실시간 화면 보기

def display_digit(digit):
    for i, pin in enumerate(segment_pins):
        GPIO.output(pin, digit_map[digit][i])

def buzzer_on():
    pwm.ChangeFrequency(523) #도
    time.sleep(1)
    pwm.ChangeFrequency(659) #미
    time.sleep(1)
    pwm.ChangeFrequency(783) #솔
    time.sleep(1)

def buzzer_off():
    pwm.ChangeFrequency(0)

def take_photo():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    filename = f"photo_{timestamp}.jpg"
    camera.capture(filename)
    print(f"사진 촬영: {filename}")

def main():
    try:
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, 120 - int(elapsed_time))
            
            #7segment 활용하는 부분
            if remaining_time >= 0 and remaining_time <= 9:
                display_digit(remaining_time // 10)
                time.sleep(0.1)
           
            # 120초가 지나거나 버튼이 눌리면 사진 찍기
            if elapsed_time >= 120 or not GPIO.input(button_pin):
                buzzer_on()
                take_photo()
                buzzer_off()
                start_time = time.time()

    except KeyboardInterrupt:
        pass

    finally:
        camera.stop_preview()  # OpenCV로 실시간 화면 중지
        GPIO.cleanup()
        camera.close()

if __name__ == "__main__":
    main()
