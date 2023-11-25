import cv2
import numpy as np
from path import IMG_DIR, PATH


def merge(
    img1: np.ndarray,
    img2: np.ndarray,
    img3: np.ndarray,
    img4: np.ndarray,
) -> None:

    # img_frame 불러오기
    img_frame = cv2.imread(f"{PATH}/images/blackframe_big.png")

    # 이미지 크기를 맞춰줌
    img1_resized = cv2.resize(img1, (704*4, 528*4))
    img2_resized = cv2.resize(img2, (704*4, 528*4))
    img3_resized = cv2.resize(img3, (704*4, 528*4))
    img4_resized = cv2.resize(img4, (704*4, 528*4))

    # img_frame의 특정 영역에 이미지 덧씌우기
    x_offset1, y_offset1 = 144, 152
    img_frame[y_offset1:y_offset1 + img1_resized.shape[0],
              x_offset1:x_offset1 + img1_resized.shape[1]] = img1_resized

    x_offset2, y_offset2 = 144, 2352
    img_frame[y_offset2:y_offset2 + img2_resized.shape[0],
              x_offset2:x_offset2 + img2_resized.shape[1]] = img2_resized

    x_offset3, y_offset3 = 144, 4552
    img_frame[y_offset3:y_offset3 + img3_resized.shape[0],
              x_offset3:x_offset3 + img3_resized.shape[1]] = img3_resized

    x_offset4, y_offset4 = 144, 6752
    img_frame[y_offset4:y_offset4 + img4_resized.shape[0],
              x_offset4:x_offset4 + img4_resized.shape[1]] = img4_resized

    # 이미지 저장
    cv2.imwrite(f"{IMG_DIR}/img.jpg", img_frame)
