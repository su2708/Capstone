import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier("Driver_Cam/haarcascade/haarcascade_frontalface_default.xml")

eye_cascade = cv2.CascadeClassifier("Driver_Cam/haarcascade/haarcascade_eye.xml")

def test(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 1)
    print("Number of faces detected: " + str(len(faces)))
    
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 1)

    return img
