import socket
import cv2
import time
from Driver_Cam.driver_status import driver_status
from audio import turn_on_alarm1 as alarm1
from audio import turn_on_alarm2 as alarm2

WIDTH = 640
HEIGHT = 480

cam = cv2.VideoCapture(0)
cam.set(3, WIDTH)
cam.set(4, HEIGHT)

HOST = '192.168.0.8' # rpi4 ip address
#HOST = '192.168.137.137' # rpi4 ip address
PORT = 12345 # Pick an open Port (1000 + recommended), must match the server port

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((HOST, PORT))

pre_status = ''
drowsy_count = 0
frame_count = 0
start_time = time.time()

while True:
    success, image = cam.read()
    command = "nothing happened"
    if not success:
        print("Rpi3 read failed")
        continue
        
    image = cv2.flip(image, 1)
    image, status = driver_status(image)
    
    # 3초 동안 command가 drowsy면 command = drowsiness warning
    if pre_status != status:
        pre_status = status
        drowsy_count = 0
    elif pre_status == 'd' and status == 'd':
        drowsy_count += 1
        if drowsy_count >= 2:
            #command = 'w'   # drowsiness warning!
            print("Driver Drowsiness Warning!")
            alarm1()
            drowsy_count = 0
    else:
        pass
    
    end_time = time.time()
    frame_count += 1
    
    time_interval = end_time - start_time
    fps = frame_count / time_interval
    
    cv2.putText(image, "FPS {:.2f}".format(fps), (400, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Rpi3 webcam", image)
    
    frame_count = 0
    start_time = time.time()
    
    # if press 'q', system closed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Rpi3 quited")
        command = "quit"
        break
    
    # socket communication part
    try:
        soc.send(command.encode('utf-8'))
        reply = soc.recv(1024).decode('utf-8')
        if reply == "Quit chatting":
            break
        elif reply == "ped":
            print("Pedestrian detected")
            alarm2()
        elif reply == "car close":
            print("The car ahead is close")
            alarm2()

    except socket.error as e:
        print(f"Socket error: {e}")
        break

cam.release()

cv2.destroyAllWindows()

