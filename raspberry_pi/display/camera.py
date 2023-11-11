import cv2
import time
import RPi.GPIO as GPIO

# GPIO 핀 번호 설정
button_pin = 17 

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 카메라 모듈 초기화
for i in range(1, 5):
    cap = cv2.VideoCapture(0)

    # 카메라 해상도 설정
    cap.set(3, 704)  # 너비, 가로 크기
    cap.set(4, 528)  # 높이, 세로 크기

    # 버튼을 누르면 사진을 찍도록 하는 변수
    take_photo = False
    start_time = time.time()

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 프레임 디스플레이
        cv2.imshow('Camera Module Display', frame)
        
        if GPIO.input(button_pin) == GPIO.LOW:
            take_photo = True

        # 120초가 지나면 사진을 찍기
        elapsed_time = time.time() - start_time
        if elapsed_time > 120:
            take_photo = True

        # 'q' 키나 버튼을 누르면 종료
        key = cv2.waitKey(1)
        if take_photo:
            break

    # 사진 찍기
    if take_photo:
        ret, frame = cap.read()
        photo_path = f"raspberry_pi/images/example{i}.png"
        cv2.imwrite(photo_path, frame)
        print(f"Photo saved at {photo_path}")

    # 작업 완료 후 리소스 해제
    cap.release()
    cv2.destroyAllWindows()


#! sudo modprobe bcm2835-v4l2으로 카메라 모듈 활성화