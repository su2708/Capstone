import numpy as np
import mediapipe as mp
import cv2
import itertools
from mediapipe.framework.formats import landmark_pb2
from scipy.spatial import distance

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

def left_ear_algorithm(image, left_eye_indices, landmarks):
    # left eye top indices: 0, 15, 14
    # left eye bottom indices: 7, 8, 10
    # left eye horizontal indices: 1, 4
    
    # get average height of left eye
    left_vertical_top = [0, 15, 14]
    left_top_coordinates = []
    for i, idx in enumerate(left_vertical_top):
        x, y = landmarks.landmark[left_eye_indices[idx]].x, landmarks.landmark[left_eye_indices[idx]].y
        left_top_coordinates.append((x, y))
    
    left_vertical_bottom = [7, 8, 10]
    left_bottom_coordinates = []
    for i, idx in enumerate(left_vertical_bottom):
        x, y = landmarks.landmark[left_eye_indices[idx]].x, landmarks.landmark[left_eye_indices[idx]].y
        left_bottom_coordinates.append((x, y))
    
    vertical_distance_avg = float(0.0)
    for i in range(len(left_top_coordinates)):
        d = distance.euclidean(left_top_coordinates[i], left_bottom_coordinates[i])
        vertical_distance_avg += d
    vertical_distance_avg = vertical_distance_avg / 3.0
    
    # get width of left eye
    left_horizontal = [1, 4]
    left_horizontal_coordinates = []
    for i, idx in enumerate(left_horizontal):
        x, y = landmarks.landmark[left_eye_indices[idx]].x, landmarks.landmark[left_eye_indices[idx]].y
        left_horizontal_coordinates.append((x, y))
        
    horizontal_distance = distance.euclidean(left_horizontal_coordinates[0], left_horizontal_coordinates[1])
    
    # EAR(Eye Aspect Ratio) = the average heights of eye / the width of eye
    ear = vertical_distance_avg / horizontal_distance
    
    threshold = 0.2
    if ear < threshold:
        # eye is closed
        return 0
    else:
        # eye is open
        return 1

def right_ear_algorithm(image, right_eye_indices, landmarks):
    # right eye top indices: 1, 2, 3
    # right eye bottom indices: 13, 11, 10
    # right eye horizontal indices: 7, 6
    
    # get average height of right eye
    right_vertical_top = [1, 2, 3]
    right_top_coordinates = []
    for i, idx in enumerate(right_vertical_top):
        x, y = landmarks.landmark[right_eye_indices[idx]].x, landmarks.landmark[right_eye_indices[idx]].y
        right_top_coordinates.append((x, y))
    
    right_vertical_bottom = [13, 11, 10]
    right_bottom_coordinates = []
    for i, idx in enumerate(right_vertical_bottom):
        x, y = landmarks.landmark[right_eye_indices[idx]].x, landmarks.landmark[right_eye_indices[idx]].y
        right_bottom_coordinates.append((x, y))
    
    vertical_distance_avg = float(0.0)
    for i in range(len(right_top_coordinates)):
        d = distance.euclidean(right_top_coordinates[i], right_bottom_coordinates[i])
        vertical_distance_avg += d
    vertical_distance_avg = vertical_distance_avg / 3.0
    
    # get width of right eye
    right_horizontal = [7, 6]
    right_horizontal_coordinates = []
    for i, idx in enumerate(right_horizontal):
        x, y = landmarks.landmark[right_eye_indices[idx]].x, landmarks.landmark[right_eye_indices[idx]].y
        right_horizontal_coordinates.append((x, y))
        
    horizontal_distance = distance.euclidean(right_horizontal_coordinates[0], right_horizontal_coordinates[1])
    
    # EAR(Eye Aspect Ratio) = the average heights of eye / the width of eye
    ear = vertical_distance_avg / horizontal_distance
    
    threshold = 0.2
    if ear < threshold:
        # eye is closed
        return 0
    else:
        # eye is open
        return 1
    

def draw_eye_box(image, eye_indices, landmarks, eye_status):
    # eye box basic settings
    color = (255, 255, 255)
    thickness = 2
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    lineType = cv2.LINE_AA
    message = "open" if eye_status == 1 else "close"
    
    max_x, min_x = float('-inf'), float('inf')
    max_y, min_y = float('-inf'), float('inf')
    
    # get max & min coordinates of eye
    for eye_index in eye_indices:
        landmark = landmarks.landmark[eye_index]
        if max_x <= landmark.x:
            max_x = landmark.x
        elif min_x > landmark.x:
            min_x = landmark.x
        
        if max_y <= landmark.y:
            max_y = landmark.y
        elif min_y > landmark.y:
            min_y = landmark.y
    
    # set max & min coordinates of eye box
    box_max_x, box_min_x = int(max_x * image.shape[1]) + 10, int(min_x * image.shape[1]) - 10
    box_max_y, box_min_y = int(max_y * image.shape[0]) + 10, int(min_y * image.shape[0]) - 10
    
    top_left = (box_min_x, box_min_y)
    bottom_right = (box_max_x, box_max_y)
    
    # draw eye box
    cv2.putText(image, message, top_left, fontFace, fontScale, color, thickness, lineType)
    cv2.rectangle(image, top_left, bottom_right, color, thickness)
    
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
    
        # FACEMESH_RIGHT_EYE display the left eye on the screen
        LEFT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
        LEFT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()
        
        # FACEMESH_LEFT_EYE display the right eye on the screen
        RIGHT_EYE_INDICES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
        RIGHT_EYE_LANDMARKS = landmark_pb2.NormalizedLandmarkList()

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                lms = face_landmarks.landmark

                # Make a LEFT_EYE_LANDMARKS
                for index in LEFT_EYE_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    LEFT_EYE_LANDMARKS.landmark.extend([landmark])

                # Make a RIGHT_EYE_LANDMARKS
                for index in RIGHT_EYE_INDICES:
                    landmark = landmark_pb2.NormalizedLandmark()
                    landmark.x = lms[index].x
                    landmark.y = lms[index].y
                    landmark.z = lms[index].z
                    RIGHT_EYE_LANDMARKS.landmark.extend([landmark])
                
                # Draw borders around Face, Eyes and Lips
                # mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=face_landmarks,
                #     connections=mp_face_mesh.FACEMESH_CONTOURS,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=mp_drawing_styles
                #     .get_default_face_mesh_contours_style()
                # )
                
                # Draw iris
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style()
                )
                
                # Draw Left eye points
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=LEFT_EYE_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                )
                # Draw Right eye points
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=RIGHT_EYE_LANDMARKS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1, circle_radius=1),
                )
                
                # EAR algorithm part
                left_eye_status = left_ear_algorithm(image, LEFT_EYE_INDICES, face_landmarks)
                right_eye_status = right_ear_algorithm(image, RIGHT_EYE_INDICES, face_landmarks)
                
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