from PyQt5.QtGui import QImage, QImageReader
import numpy as np
import cv2

def check(qimg):
    # QImage 객체 생성 또는 이미지 파일에서 로드
    image = qimg # 예시로 이미지 파일을 로드하거나 QImage를 생성

    # QImage를 NumPy 배열로 변환
    width, height = image.width(), image.height()
    bytes_per_line = image.bytesPerLine()
    format_ = image.format()

    if format_ == QImage.Format_RGB888:
        # QImage가 RGB888 형식인 경우 (8-bit R, 8-bit G, 8-bit B)
        buffer = image.bits().asstring(width * height * 3)  # QImage 데이터를 바이트 스트링으로 추출
        numpy_array = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 3)
        print('format rgb888')
        #bgr_image = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
        # height, width, _ = bgr_image.shape
        # resized_image = cv2.resize(bgr_image, (int(width * 0.5), int(height * 0.5)))
        # cv2.imwrite('output image.jpg', resized_image)
    
    else:
        # 다른 형식의 QImage에 대한 처리 (필요에 따라 추가적인 처리 필요)
        raise ValueError("지원하지 않는 QImage 형식입니다.")

    # 이제 numpy_array에 QImage 데이터가 NumPy 배열로 저장됩니다.
