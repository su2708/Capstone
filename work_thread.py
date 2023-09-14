from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QWidget
from picamera2 import Picamera2
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QThread, Qt
import RPi.GPIO as gp
import time
import os

width = 320
height = 240 

adapter_info = {  
    "A" : {   
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x04",
        "gpio_sta":[0,0,1],
    }, "B" : {
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x05",
        "gpio_sta":[1,0,1],
    }
}

class WorkThread(QThread):

    def __init__(self):
        super(WorkThread,self).__init__()
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)


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

    def run(self):
        global picam2
        
        flag = False

        for item in {"A","B"}:
            try:
                self.select_channel(item)
                self.init_i2c(item)
                time.sleep(0.5) 
                if flag == False:
                    flag = True
                else :
                    picam2.close()
                print("init1 "+ item)
                picam2 = Picamera2()
                picam2.configure(picam2.create_still_configuration(main={"size": (320, 240),"format": "BGR888"},buffer_count=2)) 
                picam2.start()
                time.sleep(2)
                picam2.capture_array(wait=False)
                time.sleep(0.1)
            except Exception as e:
                print("except: "+str(e))

        while True:
            for item in {"A","B"}:
                self.select_channel(item)
                time.sleep(0.02)
                try:
                    buf = picam2.capture_array()
                    cvimg = QImage(buf, width, height,QImage.Format_RGB888)
                    pixmap = QPixmap(cvimg)
                    if item == 'A':
                        image_label.setPixmap(pixmap)
                    elif item == 'B':
                        image_label2.setPixmap(pixmap)
                except Exception as e:
                    print("capture_buffer: "+ str(e))
                    
class MultiCamWindow(QWidget):
    # Esc key를 누르면 카메라 실행 창이 꺼지는 함수
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

app = QApplication([])
window = MultiCamWindow()
layout_h = QHBoxLayout()
layout_v = QVBoxLayout()
image_label = QLabel()
image_label2 = QLabel()