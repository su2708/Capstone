from PyQt5.QtWidgets import QApplication
from test_thread import MultiCamWindow  # your_main_script에는 원래 코드의 모듈 이름이 들어갑니다.
import sys

model_weights = '/home/pi4/Capstone/drowsiness_lite.tflite'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiCamWindow(model_path=model_weights)  # model_weights 변수는 필요에 따라 수정하세요.
    window.show()
    sys.exit(app.exec_())
