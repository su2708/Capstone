import sys
import time
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QWidget

# define Worker Thread class
class WorkerThread(QThread):
    # 작업이 완료되었을 때 시그널을 보내기 위한 시그널 객체
    finished = pyqtSignal()
    
    def run(self):
        # 시간이 오래 걸리는 작업 수행
        time.sleep(5)
        # 작업이 완료되었음을 시그널로 알림
        self.finished.emit()
        
# 메인 윈도우 클래스 정의
class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QThread example")
        
        layout = QVBoxLayout()
        self.button = QPushButton("start")
        
        self.button.clicked.connect(self.startWorkerThread)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
    def startWorkerThread(self):
        # Worker 스레드 객체 생성
        self.thread = WorkerThread()
        
        # 작업이 완료되면 finished 시그널에 대한 슬롯 연결
        self.thread.finished.connect(self.workerThreadFinished)
        
        # Worker 스레드 시작
        self.thread.start()
        # 버튼 비활성화
        self.button.setEnabled(False)
        
    def workerThreadFinished(self):
        # 작업이 완료되면 스레드 정리 및 버튼 활성화
        self.thread.quit()
        self.thread.wait()
        self.button.setEnabled(True)
        print("worker thread finished")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())