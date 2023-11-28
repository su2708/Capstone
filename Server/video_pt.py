import cv2
import time
import torch
from torchvision import transforms
from PIL import Image
from pathlib import Path
from audio_test import turn_on_alarm1 as alarm1
from audio_test import turn_on_alarm2 as alarm2
from cnn_tflite import curve

start_x = 200
end_x = 1070
start_y = 400
end_y = 720

def load_custom_model(model_path='best2.pt'):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    return model

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
    
    # Initialize YOLOv5 model
    model = load_custom_model()
    
    # Initialize FPS
    frame_count = 0
    start_time = time.time()
    name = ''
    
    while True:
        success, image = cam.read()
        if not success:
            print("Fail to read webcam")
            continue
        
        # lane detection
        roi = image[start_y:end_y, start_x:end_x]
        predicted_class = curve(roi)
        
        # yolov5 part
        results = model(image, size=160)
        
        if len(results.xyxy[0]) == 0:
            print("No objects detected.")
        else:
            print(results.pandas().xyxy[0])
            class_name = results.pandas().xyxy[0]['name']
            class_conf = results.pandas().xyxy[0]['confidence']
            class_xmax = results.pandas().xyxy[0]['xmax']
            class_xmin = results.pandas().xyxy[0]['xmin']
            class_ymax = results.pandas().xyxy[0]['ymax']
            class_ymin = results.pandas().xyxy[0]['ymin']
            name = class_name[0]
            conf = class_conf[0]
            xmax = class_xmax[0]
            xmin = class_xmin[0]
            ymax = class_ymax[0]
            ymin = class_ymin[0]
            print(f"{name} {conf:.2f}")
            # calculate_area
            if len(name) != 0:
                x = xmax - xmin
                y = ymax - ymin
                area = x*y
                print(area)
            if name == 'ped':
                #alarm2()
                x = xmax - xmin
                y = ymax - ymin
                area = x*y
                if area >= 8000 and area <=15000:
                    print("Pedestrian: ", area)
            elif name == 'car_back':
                x = xmax - xmin
                y = ymax - ymin
                area = x*y
                if area >= 15000 and area <=30000:
                    print("Car back: ", area)
            if conf >= 0.8:
                print(f"{name} {conf:.2f}, over 80 conf")
        
        end_time = time.time()
        frame_count += 1
        
        time_interval = end_time - start_time

        fps = frame_count / time_interval
        
        cv2.putText(image, predicted_class, (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(image, "FPS: {:.2f}".format(fps), (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
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



