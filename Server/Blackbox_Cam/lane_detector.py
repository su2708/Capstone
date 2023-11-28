import cv2
import numpy as np
import utils

def getLaneCurve(img):
    
    ## STEP 1
    imgThres = utils.thresholding(img)
    
    return None

if __name__ == '__main__':
    cap = cv2.VideoCapture('D:\과기대\캡스톤디자인\Capstone Design\Capstone\Blackbox_Cam\challenge_video.mp4')
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (480, 240))
        
        cv2.imshow('Video', img)
        cv2.waitKey(1)