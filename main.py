import mediapipe as mp
import cv2
import itertools
from mediapipe.framework.formats import landmark_pb2
from get_EAR_status import get_ear_status
from draw_eye_box import draw_eye_box

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    
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

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
    RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
    
    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

    if results.multi_face_landmarks is not None:
        for face_landmarks in results.multi_face_landmarks:
            lms = face_landmarks.landmark
            
            # Draw borders around Face, Eyes and Lips
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style()
            )
            
            # Draw iris
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_iris_connections_style()
            )
            
            # EAR algorithm part
            '''
            left eye top indices: 1, 2, 3
            left eye bottom indices: 13, 11, 10
            left eye width indices: 7, 6
            '''
            L_eye_top = [1, 2, 3]
            L_eye_bottom = [13, 11, 10]
            L_eye_width = [7, 6]
            
            '''
            right eye top indices: 0, 15, 14
            right eye bottom indices: 7, 8, 10
            right eye width indices: 1, 4
            '''
            R_eye_top = [0, 15, 14]
            R_eye_bottom = [7, 8, 10]
            R_eye_width = [1, 4]

            left_eye_status = get_ear_status(LEFT_EYE_INDICES, L_eye_top, L_eye_bottom, L_eye_width, face_landmarks)
            right_eye_status = get_ear_status(RIGHT_EYE_INDICES, R_eye_top, R_eye_bottom, R_eye_width, face_landmarks)
            
            # Draw eye boxes
            draw_eye_box(image, LEFT_EYE_INDICES, face_landmarks, left_eye_status)
            draw_eye_box(image, RIGHT_EYE_INDICES, face_landmarks, right_eye_status)
            
        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    else:
        print("No faces detected.")
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
        results = face_mesh.process(image)
    
        LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
        # LEFT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
        # RIGHT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        LIP_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LIPS)))
        LIP_LANDMARKS = landmark_pb2.NormalizedLandmarkList()

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
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

                # Make a RIGHT_EYE_LANDMARKS
                '''
                for index in RIGHT_EYE_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    RIGHT_EYE_LANDMARKS.landmark.extend([landmark])
                '''
                
                # Make a LIP_LANDMARKS
                for index in LIP_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    LIP_LANDMARKS.landmark.extend([landmark])
                
                # Draw Lips
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=LIP_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                )
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
                
                # Draw Left eye points
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=LEFT_EYE_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                )
                '''
                
                # Draw Right eye points
                '''
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=RIGHT_EYE_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1, circle_radius=1),
                )
                '''
                
                # EAR algorithm part
                '''
                left eye top indices: 1, 2, 3
                left eye bottom indices: 13, 11, 10
                left eye width indices: 7, 6
                '''
                L_eye_top = [1, 2, 3]
                L_eye_bottom = [13, 11, 10]
                L_eye_width = [7, 6]
                
                '''
                right eye top indices: 0, 15, 14
                right eye bottom indices: 7, 8, 10
                right eye width indices: 1, 4
                '''
                R_eye_top = [0, 15, 14]
                R_eye_bottom = [7, 8, 10]
                R_eye_width = [1, 4]

                left_eye_status = get_ear_status(LEFT_EYE_INDICES, L_eye_top, L_eye_bottom, L_eye_width, face_landmarks)
                right_eye_status = get_ear_status(RIGHT_EYE_INDICES, R_eye_top, R_eye_bottom, R_eye_width, face_landmarks)
                
                # Draw eye boxes
                draw_eye_box(image, LEFT_EYE_INDICES, face_landmarks, left_eye_status)
                draw_eye_box(image, RIGHT_EYE_INDICES, face_landmarks, right_eye_status)
                
            cv2.imshow('MediaPipe Face Mesh', image)
            if cv2.waitKey(5) & 0xFF == 27:
                cv2.destroyAllWindows()
                break
        else:
            print("No faces detected.")
            break
cap.release()
"""