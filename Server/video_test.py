import cv2
import time
from picamera2 import Picamera2

def main():
    # 웹캠 초기화
    cam_num = 0
    cam = cv2.VideoCapture(cam_num)
    ret, frame = cam.read()
    if ret:
        print("This device is rpi3")
        cam.release()
        cam = cv2.VideoCapture(cam_num)
    elif not ret:
        print("This device is rpi4")
        cam.release()
        cam_num = 4 # 2 or 4
        cam = cv2.VideoCapture(cam_num)

    cam.set(3, 640)
    cam.set(4, 480)
    
    # Initialize FPS
    frame_count = 0
    start_time = time.time()
    
    while True:
        success, image = cam.read()
        if not success:
            print("Fail to read webcam")
            continue
        
        end_time = time.time()
        frame_count += 1
        
        time_interval = end_time - start_time

        fps = frame_count / time_interval
        cv2.putText(image, "FPS: {:.2f}".format(fps), (400, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        frame_count = 0
        start_time = time.time()
            
        cv2.imshow('Webcam', image)
        
        if cv2.waitKey(1) == ord('q'):
            print('Quitting webcam')
            break
    
    # 웹캠 해제
    cam.release()
    
    # OpenCV 창 닫기
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


