import mediapipe as mp
import cv2
import time
import itertools
from Driver_Cam.EAR import get_EAR
from Driver_Cam.eye_crop import crop_eye

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1)
    
# Face mesh setting part
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True, 
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

def driver_status(image):
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

    # Eye outlines   
    LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
    RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
    
    # Eyes status
    status = ""
    
    if results.multi_face_landmarks is not None:
        for face_landmarks in results.multi_face_landmarks:
            # EAR algorithm part
            left_eye_status = get_EAR(LEFT_EYE_INDICES, face_landmarks, side="left")
            right_eye_status = get_EAR(RIGHT_EYE_INDICES, face_landmarks, side="right")
            
            # Draw eye boxes
            image = crop_eye(image, LEFT_EYE_INDICES, face_landmarks, left_eye_status)
            image = crop_eye(image, RIGHT_EYE_INDICES, face_landmarks, right_eye_status)

            # Drowsy or Awake
            if left_eye_status == 1 or right_eye_status == 1:
                status = "a"  # driver awake
            else:
                status = "d"  # driver drowsy
    else:
        status = "Can't detect face!"
        
    return image, status
