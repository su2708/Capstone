import sys
import cv2
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from Driver_Cam import haarcascade_test

class WebcamThread(QObject):
    image_data = pyqtSignal(QImage)

    def start(self):
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.start()

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read webcam")
                break

            rgb_image = haarcascade_test.test(frame)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_data.emit(qt_image)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Viewer")
        self.image_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.thread = WebcamThread()
        self.thread.image_data.connect(self.update_image)
        self.thread.start()

    def update_image(self, image):
        self.image_label.setPixmap(QPixmap.fromImage(image))
        self.image_label.setScaledContents(True)

    # Esc key를 누르면 카메라 실행 창이 꺼지는 함수
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
