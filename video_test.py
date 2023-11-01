import cv2
from picamera2 import Picamera2

def main():
    # 웹캠 초기화
    cam = cv2.VideoCapture(2) # 2 or 4
    cam.set(3, 640)
    cam.set(4, 480)
    
    while True:
        success, image = cam.read()
        if not success:
            print("Fail to read webcam")
            continue
        image = cv2.flip(image, flipCode=1)
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


