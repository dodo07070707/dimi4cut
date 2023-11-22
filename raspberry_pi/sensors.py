import RPi.GPIO as g
import time
import cv2
import numpy as np

# GPIO 설정
button_pin = 17  # 버튼 핀
buzzer_pin = 18  # 부저 핀
segment_pins = (21, 20, 16, 12, 25, 24, 23, 22)  # 7-Segment 핀
led_pin = 26  # LED 핀

# GPIO 초기화
g.setwarnings(False)
g.setmode(g.BCM)
g.setup(button_pin, g.IN, pull_up_down=g.PUD_UP)
g.setup(buzzer_pin, g.OUT)
g.setup(segment_pins, g.OUT)
g.setup(led_pin, g.OUT)

buzzerpwm = g.PWM(buzzer_pin, 1000)
buzzerpwm.start(50)

# 7-Segment Display 디지트 맵
digit_map = {
    '0' : (1, 1, 1, 1, 1, 1, 0, 0),
    '1' : (0, 1, 1, 0, 0, 0, 0, 0),
    '2' : (1, 1, 0, 1, 1, 0, 1, 0),
    '3' : (1, 1, 1, 1, 0, 0, 1, 0),
    '4' : (0, 1, 1, 0, 0, 1, 1, 0),
    '5' : (1, 0, 1, 1, 0, 1, 1, 0),
    '6' : (1, 0, 1, 1, 1, 1, 1, 0),
    '7' : (1, 1, 1, 0, 0, 1, 0, 0),
    '8' : (1, 1, 1, 1, 1, 1, 1, 0),
    '9' : (1, 1, 1, 1, 0, 1, 1, 0),
}


# 카메라 초기화
cap = cv2.VideoCapture(0)  # OpenCV 카메라 객체 생성
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

# LED 초기화
ledpwm = g.PWM(led_pin, 100)  # PWM 주파수 설정
ledpwm.start(0)  # PWM 시작, 초기 밝기 0으로 설정

for segment in segment_pins:
    g.setup(segment, g.OUT)
    g.output(segment, False)
    

def display_digit(digit):
    print(digit)
    s = str(digit)
    for loop in range(0,8):
        g.output(segment_pins[loop], digit_map[s][loop])

def buzzer_on():
    buzzerpwm.ChangeFrequency(523)  # 도
    time.sleep(1)
    buzzerpwm.ChangeFrequency(659)  # 미
    time.sleep(1)
    buzzerpwm.ChangeFrequency(783)  # 솔
    time.sleep(1)

def buzzer_off():
    buzzerpwm.ChangeFrequency(1)

def take_photo():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    filename = f"photo_{timestamp}.jpg"
    
    # OpenCV를 사용하여 프레임을 캡처
    ret, frame = cap.read()
    
    # 이미지 저장
    cv2.imwrite(filename, frame)
    print(f"took photo: {filename}")

def main():
    order_number = 0
    while True:
        order_number += 1
        try:
            start_time = time.time()
            while True:
                # 지난 시간 계산
                elapsed_time = time.time() - start_time
                remaining_time = max(0, 20 - int(elapsed_time))
                
                # 7segment 활용하는 부분
                if remaining_time >= 0 and remaining_time <= 9:
                    display_digit(remaining_time)
                    time.sleep(0.1)
                    
                print(elapsed_time, order_number)
                # 120초가 지나거나 버튼이 눌리면 사진 찍기
                if elapsed_time >= 20 or not g.input(button_pin):
                    buzzer_on()
                    take_photo()
                    buzzer_off()
                    time.sleep(1)
                    break
                    
        except KeyboardInterrupt:
            pass

        finally:
            cap.release()  # 카메라 객체 해제
            cv2.destroyAllWindows()  # OpenCV 창 닫기

if __name__ == "__main__":
    main()
