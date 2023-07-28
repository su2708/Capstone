'''
운전자 상태 = 얼굴인식 + 물체인식

1. 얼굴인식
 - 운전자가 어딜 보고 있는지 파악
 - 운전자가 눈을 감고있는지 파악
 
2. 물체인식
 - 운전자를 보는 카메라 시야 안에 휴대폰으로 추정되는 것이 보이는지 아닌지
'''
import mediapipe as mp
import cv2
import itertools
import time
from mediapipe.framework.formats import landmark_pb2
from EAR import get_EAR
from eye_crop import crop_eye
from eye_tracking import track_eyes
# main.py에서 실행하려면
# from Driver_Cam.EAR import get_EAR
# from Driver_Cam.eye_crop import crop_eye

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

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    start = time.time()

    # FACE MESH PART

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    fm_results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

    # Eye outlines   
    LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
    RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))

    # Iris outlines
    IRIS_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_IRISES)))
    IRIS_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
    
    if fm_results.multi_face_landmarks is not None:
        for face_landmarks in fm_results.multi_face_landmarks:
            lms = face_landmarks.landmark

            # Make IRIS_LANDMARKS
            for index in IRIS_INDICES:
                landmark = landmark_pb2.NormalizedLandmark()
                landmark.x = lms[index].x
                landmark.y = lms[index].y
                landmark.z = lms[index].z
                IRIS_LANDMARKS.landmark.extend([landmark])
            
            # Eye tracking part
            track_eyes(image, face_landmarks, IRIS_INDICES)

            # EAR algorithm part
            left_eye_status = get_EAR(LEFT_EYE_INDICES, face_landmarks, side="left")
            right_eye_status = get_EAR(RIGHT_EYE_INDICES, face_landmarks, side="right")
            
            # Draw eye boxes
            crop_eye(image, LEFT_EYE_INDICES, face_landmarks, left_eye_status)
            crop_eye(image, RIGHT_EYE_INDICES, face_landmarks, right_eye_status)
            
        end = time.time()
        total_time = end - start
        fps = 1/ total_time
        cv2.putText(image, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()

# Close the solution
face_mesh.close()

"""
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        fm_results = face_mesh.process(image)
    
        # Left eye outlines
        LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
        LEFT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        # Right eye outlines
        RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
        RIGHT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        # Lips outlines
        LIP_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LIPS)))
        LIP_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        # Face outline
        OUTLINE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_FACE_OVAL)))
        OUTLINE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()

        # Iris outlines
        IRIS_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_IRISES)))
        IRIS_LANDMARKS = landmark_pb2.NormalizedLandmarkList()

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
        if fm_results.multi_face_landmarks is not None:
            for face_landmarks in fm_results.multi_face_landmarks:
                lms = face_landmarks.landmark

                # Make a LEFT_EYE_LANDMARKS
                '''
                for index in LEFT_EYE_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    LEFT_EYE_LANDMARKS.landmark.extend([landmark])
                '''
                
                # Draw Left eye points
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=LEFT_EYE_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                )
                '''

                # Make a RIGHT_EYE_LANDMARKS
                '''
                for index in RIGHT_EYE_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    RIGHT_EYE_LANDMARKS.landmark.extend([landmark])
                '''
                
                # Draw Right eye points
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=RIGHT_EYE_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1, circle_radius=1),
                )
                '''
                
                # Make a LIP_LANDMARKS
                '''
                for index in LIP_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    LIP_LANDMARKS.landmark.extend([landmark])
                '''
                
                # Draw Lips
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=LIP_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                )
                '''
                    
                # Make OUTLINE_LANDMARKS
                '''
                for index in OUTLINE_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    OUTLINE_LANDMARKS.landmark.extend([landmark])
                '''
                
                # Draw face outline
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=OUTLINE_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                )
                '''
                
                # Make IRIS_LANDMARKS
                '''
                for index in IRIS_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    IRIS_LANDMARKS.landmark.extend([landmark])
                '''
                
                # Draw iris
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style()
                )
                '''
                
                # Draw specific iris point
                '''
                print(len(IRIS_INDICES))
                point_index = 0
                chosen_point = lms[IRIS_INDICES[point_index]]
                image_height, image_width, _ = image.shape
                point_x = int(chosen_point.x * image_width)
                point_y = int(chosen_point.y * image_height)
                cv2.circle(image, (point_x, point_y), radius=5, color=(255, 0, 0))
                '''
                
                # Draw face landmarks
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                '''
                
                # Draw borders around Face, Eyes and Lips
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style()
                )
                '''
                
                # EAR algorithm part
                left_eye_status = EAR(LEFT_EYE_INDICES, L_eye_top, L_eye_bottom, L_eye_width, face_landmarks)
                right_eye_status = EAR(RIGHT_EYE_INDICES, R_eye_top, R_eye_bottom, R_eye_width, face_landmarks)
                
                # Draw eye boxes
                crop_eye(image, LEFT_EYE_INDICES, face_landmarks, left_eye_status)
                crop_eye(image, RIGHT_EYE_INDICES, face_landmarks, right_eye_status)
                
            cv2.imshow('MediaPipe Face Mesh', image)
            if cv2.waitKey(5) & 0xFF == 27:
                cv2.destroyAllWindows()
                break
        else:
            print("No faces detected.")
            break
cap.release()
"""