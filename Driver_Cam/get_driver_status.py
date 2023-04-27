import mediapipe as mp
import cv2
import itertools
from mediapipe.framework.formats import landmark_pb2
from get_EAR import EAR
from crop_eye import crop_eye
# main.py에서 실행하려면
# from Driver_Cam.get_EAR import EAR
# from Driver_Cam.crop_eye import crop_eye


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    
# Face mesh setting part
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True, 
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Object detection setting part
mp_objectron = mp.solutions.objectron
objectron = mp_objectron.Objectron(
    static_image_mode = False,
    max_num_objects = 5,
    min_detection_confidence = 0.5
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # FACE MESH PART

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    fm_results = face_mesh.process(image)
    obj_results = objectron.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

    # Eye outlines   
    LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
    RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
    
    # Face outline
    OUTLINE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_FACE_OVAL)))
    OUTLINE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
    
    if fm_results.multi_face_landmarks is not None:
        for face_landmarks in fm_results.multi_face_landmarks:
            lms = face_landmarks.landmark
            
            # Make a OUTLINE_LANDMARKS
            for index in OUTLINE_INDICES:
                landmark = landmark_pb2.NormalizedLandmark()
                landmark.x = lms[index].x
                landmark.y = lms[index].y
                landmark.z = lms[index].z
                OUTLINE_LANDMARKS.landmark.extend([landmark])

            # Draw face landmarks
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            # Draw face outline
            '''
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=OUTLINE_LANDMARKS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
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
            
            # Draw iris
            '''mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_iris_connections_style()
            )'''
            
            # EAR algorithm part
            left_eye_status = EAR(LEFT_EYE_INDICES, face_landmarks, side="left")
            right_eye_status = EAR(RIGHT_EYE_INDICES, face_landmarks, side="right")
            
            # Draw eye boxes
            """crop_eye(image, LEFT_EYE_INDICES, face_landmarks, left_eye_status)
            crop_eye(image, RIGHT_EYE_INDICES, face_landmarks, right_eye_status)"""
            
        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    else:
        print("No faces detected.")
        break 

    # OBJECT DETECTION PART

    if obj_results.detected_objects:
        for detected_object in obj_results.detected_objects:
            mp_drawing.draw_landmarks(image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
            mp_drawing.draw_axis(image, detected_object.rotation, detected_object.translation)
        
        
                   

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()

# Close the solution
face_mesh.close()
objectron.close()

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
    
        LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
        # LEFT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
        # RIGHT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        LIP_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LIPS)))
        LIP_LANDMARKS = landmark_pb2.NormalizedLandmarkList()

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