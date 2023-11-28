import socket
import cv2
import time
import torch
from torchvision import transforms
from PIL import Image
from pathlib import Path
from audio_test import turn_on_alarm1 as alarm1
from audio_test import turn_on_alarm2 as alarm2
from cnn_tflite import curve

WIDTH = 640
HEIGHT = 480

cam = cv2.VideoCapture(4)
cam.set(3, WIDTH)
cam.set(4, HEIGHT)

# Set server information
HOST = '192.168.0.8' # rpi4 ip address
#HOST = '192.168.137.137' # rpi4 ip address
PORT = 12345 # Pick an open Port (1000 + recommended), must match the client port

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# managing error exception
try:
    soc.bind((HOST, PORT))
except socket.error:
    print('Bind failed')
    
soc.listen(1)
print('Socket awaiting streaming')
(conn, addr) = soc.accept()
print('Connected')

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best2.pt')

frame_count = 0
start_time = time.time()

start_x = 200
end_x = 1070
start_y = 400
end_y = 720

# awaiting for message
while True:
    driver_status = conn.recv(1024).decode('utf-8')
    reply = ""
    name = ""
    success, image = cam.read()
    if not success:
        print("Rpi4 read failed")
        continue
    
    # lane detection
    roi = image[start_y:end_y, start_x:end_x]
    predicted_class = curve(roi)
    
    # yolov5 part
    results = model(image, size=160)
    
    if len(results.xyxy[0]) == 0:
        print("No objects detected.")
    else:
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
        if name == 'ped':
            #alarm2()
            x = xmax - xmin
            y = ymax - ymin
            area = x*y
            if area >= 10000:
                reply = "ped"
                print("Pedestrain detected")
        elif name == 'car_back':
            x = xmax - xmin
            y = ymax - ymin
            area = x*y
            if area >=28000:
                reply = "car close"
                print("The car ahead is close")
        if conf >= 0.8:
            print(f"{name} {conf:.2f}, over 80 conf")
        
    end_time = time.time()
    frame_count += 1
    
    time_interval = end_time - start_time
    fps = frame_count / time_interval
    
    # show the result
    cv2.putText(image, predicted_class, (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(image, "FPS {:.2f}".format(fps), (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Rpi4 webcam", image)
    
    # initialize fps
    frame_count = 0
    start_time = time.time()
    
    # if press 'q', system closed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Rpi4 quited")
        break
    
    # socket communication part  
    if not driver_status:
        print("Can't receive driver status")
        break
    
    print("Message from rpi3: ", driver_status)
    
    if driver_status == "quit":
        conn.send("Quit chatting".encode('utf-8'))
        break
    elif len(reply) == 0:
        reply="Communication is fine"
    else:
        pass
    
    # Sending reply
    conn.send(reply.encode('utf-8'))
    
# Close connection
conn.close()
cam.release()

cv2.destroyAllWindows()

