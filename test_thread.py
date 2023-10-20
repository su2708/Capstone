from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget
from picamera2 import Picamera2
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from Driver_Cam.haarcascade_test import test as haar_test
from Driver_Cam.drowsiness import detect_drowsiness as drowsiness
from Blackbox_Cam.blackbox import detect_objects_in_image as detector
import RPi.GPIO as gp
import time
import os

WIDTH = 320
HEIGHT = 320 

CAMERA_LIST = ["A", "B"]

adapter_info = {  
    "A" : {   
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x04",
        "gpio_sta":[0,0,1],
    }, "B" : {
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x05",
        "gpio_sta":[1,0,1],
    }
}

# 카메라 캡처 및 이미지 전송을 담당하는 스레드 클래스
class MultiCamThread(QObject):
    image_data = pyqtSignal(QImage, str)
    
    def __init__(self):
        # QObject의 초기화함수 실행
        super().__init__()
        
        # GPIO setting
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)
        
        # picam2 변수를 초기화
        self.picam2 = None

    def start(self):
        # QThread 객체 및 스레드 생성
        self.thread = QThread()
        
        # WebCamThread 객체를 QThread 스레드로 이동
        self.moveToThread(self.thread)
        
        # QThread 스레드가 시작하면 run 함수로 연결
        self.thread.started.connect(self.run)

        # QThread 스레드 시작
        try:
            self.thread.start()
        except Exception as e:
            print("Exception in thread start: ", str(e))

    def select_channel(self,index):
        channel_info = adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])

    def init_i2c(self,index):
        channel_info = adapter_info.get(index)
        os.system(channel_info["i2c_cmd"]) # i2c write

    # 카메라 캡처 및 이미지 전송
    def run(self):
        flag = False

        # 각 카메라 활성화
        for cam in CAMERA_LIST:
            try:
                self.select_channel(cam)
                self.init_i2c(cam)
                time.sleep(0.5) 
                if flag == False:
                    flag = True
                else :
                    self.picam2.close() # 캡처가 완료된 후 Picamera2 객체 종료
                print("init1 "+ cam)
                # Picamera2 객체 생성 및 설정 후 시작
                self.picam2 = Picamera2()
                self.picam2.configure(self.picam2.create_still_configuration(main={"size": (WIDTH, HEIGHT), "format": "BGR888"}, buffer_count=2))
                self.picam2.start()
                time.sleep(2)
                self.picam2.capture_array(wait=False) # 초기화 확인을 위한 캡처
                time.sleep(0.1)
            except Exception as e:
                print("init1: " + cam + " error: " + str(e))
        
        # FPS 초기화
        frame_count = 0
        start_time = time.time()
        
        # 실시간 이미지 캡처
        while True:
            for cam in CAMERA_LIST:
                self.select_channel(cam)
                time.sleep(0.1) # 화면 업데이트 시간
                try:
                    buf = self.picam2.capture_array() # 실시간 화면 캡처
                    if cam == "A":
                        #buf = detector(buf)
                        cvimg = QImage(buf, WIDTH, HEIGHT,QImage.Format_RGB888)
                        self.image_data.emit(cvimg, cam)
                    elif cam == "B":
                        buf = haar_test(buf)
                        cvimg = QImage(buf, WIDTH, HEIGHT,QImage.Format_RGB888)
                        self.image_data.emit(cvimg, cam)
                except Exception as e:
                    print("capture_buffer: "+ str(e))
                
                # 각 프레임마다 시간 측정
                end_time = time.time()
                frame_count += 1
                
                # 시간 간격 측정
                time_interval = end_time - start_time
                
                # 시간 간격이 1초 이상이면 FPS 계산
                if time_interval >= 1.0:
                    fps = frame_count / time_interval
                    print("FPS: {:.2f}".format(fps))
                    
                    # 초기값 재설정
                    frame_count = 0
                    start_time = time.time()

# PyQt5 위젯으로, MultiCamThread 클래스에서 전달한 이미지를 화면에 표시하는 클래스
class MultiCamWindow(QWidget):
    
    def __init__(self):
        # QWidget의 __init__함수 실행
        super().__init__()
          
        # 실행창 설정
        self.setWindowTitle('Multi Cam test')
        self.image_label_A = QLabel(self)
        self.image_label_B = QLabel(self)
        self.image_label_A.setFixedSize(WIDTH, HEIGHT)
        self.image_label_B.setFixedSize(WIDTH, HEIGHT)
        
        # 수평 레이아웃 생성 및 위젯 추가
        layout_h = QHBoxLayout()
        layout_h.addWidget(self.image_label_A)
        layout_h.addWidget(self.image_label_B)
        
        # 수직 레이아웃 생성 및 수평 레이아웃 추가
        layout_v = QVBoxLayout()
        layout_v.addLayout(layout_h)
        
        # 위젯의 레이아웃 설정
        self.setLayout(layout_v)
        self.resize(WIDTH*2 + 10, HEIGHT+10)
        
        # MultiCamThread 객체와 스레드 생성
        self.cam_thread = MultiCamThread()
        
        # image_data 시그널을 슬롯함수와 연결
        self.cam_thread.image_data.connect(self.update_image)
        
        # MultiCamThread 클래스의 start 메서드 실행
        self.cam_thread.start()
        
    # MultiCamThread 객체에서 시그널을 받으면 동작하는 슬롯함수
    def update_image(self, image, cam_type):
        if cam_type == "A":
            self.image_label_A.setPixmap(QPixmap.fromImage(image))
        else:
            self.image_label_B.setPixmap(QPixmap.fromImage(image))
    
    # Esc key를 누르면 카메라 실행 창이 꺼지는 함수
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
