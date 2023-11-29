import RPi.GPIO as g
import time
import cv2
import spidev
import numpy as np

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
# GPIO 설정
button_pin = 17  # 버튼 핀
buzzer_pin = 18  # 부저 핀
segment_pins = (21, 20, 16, 12, 25, 24, 22, 23)  # 7-Segment 핀
led_pin = 26  # LED 핀
triger = 2 #초음파 센서 핀
echo = 3
pins = {'pin_R':26, 'pin_G':19, 'pin_B':13} #RGB LED 핀


# GPIO 초기화
g.setwarnings(False)
g.setmode(g.BCM)
g.setup(button_pin, g.IN, pull_up_down=g.PUD_UP)
g.setup(buzzer_pin, g.OUT)
g.setup(segment_pins, g.OUT)
g.setup(led_pin, g.OUT)
g.setup(echo, g.IN)
g.setup(triger, g.OUT)

buzzerpwm = g.PWM(buzzer_pin, 1000)
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
    '.' : (0, 0, 0, 0, 0, 0, 0, 0),
}

colors = [0x00FF00, 0x0000FF,0xFF0000]

for i in pins:
    g.setup(pins[i], g.OUT)
    g.output(pins[i], g.HIGH)
p_R = g.PWM(pins['pin_R'], 2000)
p_G = g.PWM(pins['pin_G'], 2000)
p_B = g.PWM(pins['pin_B'], 2000)
p_R.start(0)
p_G.start(0)
p_B.start(0)

cv2.namedWindow("Life4Cut", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Life4Cut", 1280, 960)

# 카메라 초기화
cap = cv2.VideoCapture(0)  # OpenCV 카메라 객체 생성
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

for segment in segment_pins:
    g.setup(segment, g.OUT)
    g.output(segment, False)


def ReadVol(vol):
    adc = spi.xfer2([1,(0x08+vol) << 4, 0])
    data = ((adc[1]&0x03) << 8) + adc[2]
    return data

def display_digit(digit):
    print(digit)
    s = str(digit)
    for loop in range(0,8):
        g.output(segment_pins[loop], digit_map[s][loop])

def display_digit_0():
    s = '.'
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
    buzzerpwm.ChangeDutyCycle(0)

def take_photo():
    timestamp = time.startime("%Y%m%d%H%M%S")
    filename = f"photo_{timestamp}.jpg"
    
    # OpenCV를 사용하여 프레임을 캡처
    ret, frame = cap.read()
    
    # 이미지 저장
    cv2.imwrite(filename, frame)
    print(f"took photo: {filename}")
    
#microwave code
def check_person():
    a = ReadVol(0)
    print(a)
    if  a>=0 and a<=512:
        setColor(colors[1])
    else:
        setColor(colors[2])

    
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):
    R_val = (col & 0xFF0000) >> 16
    G_val = (col & 0x00FF00) >> 8
    B_val = (col & 0x0000FF) >> 0
    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)
    p_R.ChangeDutyCycle(100-R_val)
    p_G.ChangeDutyCycle(100-G_val)
    p_B.ChangeDutyCycle(100-B_val)

def main():
    order_number = 0
    while True:
        
        order_number += 1
        try:
            start_time = time.time()
            
            while True:
                # 지난 시간 계산
                elapsed_time = time.time() - start_time
                remaining_time = max(0, 50 - int(elapsed_time))
                
                # 7segment 활용하는 부분
                if remaining_time >= 0 and remaining_time <= 9:
                    display_digit(remaining_time)
                    time.sleep(0.1)
                    
                check_person()
                print(elapsed_time, order_number)
                
                # 120초가 지나거나 버튼이 눌리면 사진 찍기
                if elapsed_time >= 50 or not g.input(button_pin):
                    buzzer_on()
                    #take_photo()
                    buzzer_off()
                    display_digit_0()
                    time.sleep(1)
                    break
                    
        except KeyboardInterrupt:
            pass

        finally:
            cap.release()  # 카메라 객체 해제
            cv2.destroyAllWindows()  # OpenCV 창 닫기

if __name__ == "__main__":
    main()

