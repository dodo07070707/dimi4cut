import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('images/example1.jpg',cv2.IMREAD_COLOR) #불러오기
image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # 색입히기

cv2.imwrite('images/example1.jpg',image_rgb)

plt.imshow(image_rgb);
plt.show();