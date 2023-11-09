import cv2
import numpy as np
import matplotlib.pyplot as plt

image1 = cv2.imread('images/example1.jpg')
image2 = cv2.imread('images/example2.jpg')
image3 = cv2.imread('images/example3.jpg')
image4 = cv2.imread('images/example4.jpg')
image_frame = cv2.imread('images/blackframe.png')

# 이미지 크기를 맞춰줌
image1_resized = cv2.resize(image1, (312, 234)) # 여기 좌표 바꿔야 함
image2_resized = cv2.resize(image2, (312, 234))
image3_resized = cv2.resize(image3, (312, 234))
image4_resized = cv2.resize(image4, (312, 234))

# image_frame의 특정 영역에 이미지 덧씌우기
x_offset1, y_offset1 = 38, 44
image_frame[y_offset1:y_offset1 + image1_resized.shape[0], x_offset1:x_offset1 + image1_resized.shape[1]] = image1_resized

x_offset2, y_offset2 = 38, 294
image_frame[y_offset2:y_offset2 + image2_resized.shape[0], x_offset2:x_offset2 + image2_resized.shape[1]] = image2_resized

x_offset3, y_offset3 = 38, 544
image_frame[y_offset3:y_offset3 + image3_resized.shape[0], x_offset3:x_offset3 + image3_resized.shape[1]] = image3_resized

x_offset4, y_offset4 = 38, 794
image_frame[y_offset4:y_offset4 + image4_resized.shape[0], x_offset4:x_offset4 + image4_resized.shape[1]] = image4_resized

# 결과 이미지를 Matplotlib을 통해 출력
plt.imshow(cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB))
plt.show()
