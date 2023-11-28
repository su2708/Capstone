import cv2
import numpy as np

video = cv2.VideoCapture("D:\과기대\캡스톤디자인\Capstone Design\Capstone\Blackbox_Cam\challenge_video.mp4")
#video = cv2.VideoCapture("D:\과기대\캡스톤디자인\Capstone Design\Capstone\Blackbox_Cam\Test_seoul_360.mp4")

while True:
    ret, or_frame = video.read()        #프레임 당 이미지 읽기

    if not ret:
        break

    blurred_frame = cv2.GaussianBlur(or_frame, (5, 5), 0)   #노이즈 감소 부드러운 효과 (이미지, 커널사이즈, 표준편차)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)    #색상공간 변화 (이미지, 변환코드)

    #구름 때문에 하늘에도 선이 발생 => 이미지 일부분만 잘라서 활용하고 다시 돌려놓음

    # 너비, 높이 확인
    height, width = hsv.shape[:2]
    # print("이미지 너비: ", width) #1280, 852
    # print("이미지 높이: ", height) #720, 480
    roi_x1, roi_y1 = 0.1, 0.65
    roi_x2, roi_y2 = 0.9, 0.95

    # start_x, start_y = 100, 500
    # end_x, end_y = 1250, 710
    start_x, start_y = int(width*roi_x1), int(height*roi_y1)
    end_x, end_y = int(width*roi_x2), int(height*roi_y2)
    cropped_hsv = hsv[start_y:end_y, start_x:end_x]


    lower_y = np.array([20, 100, 140])          #색상 범위 하한 값
    upper_y = np.array([30, 255, 255])          #색상 범위 상한 값

    lower_w = np.array([0, 0, 200])             #흰선 구분 
    upper_w = np.array([180, 30, 255])          

    mask_w = cv2.inRange(cropped_hsv, lower_w, upper_w)
    mask_y = cv2.inRange(cropped_hsv, lower_y, upper_y)
    combined_mask = cv2.bitwise_or(mask_w, mask_y)
    

    edges = cv2.Canny(combined_mask, 70, 150)            #에지 검출 코드(이미지, 낮은 임계, 높은 임계)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)   
    #선 검출(에지 이미지, 거리분해능, 각도분해능, threshold, minLineLength, maxLineGap)

    # 점선을 실선처럼 이을 수 있을까?
    # 방향을 어떻게 구분해야하지? 

    #검출된 선들을 원본 이미지에 그리기
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(or_frame, (x1+100, y1+500), (x2+100, y2+500), (0, 255, 0), 5)

    cv2.imshow("frame", or_frame)
    cv2.imshow("edges", edges)

    key = cv2.waitKey(25)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()
