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

def draw_eye_box(image, eye_indices, landmarks):
    color = (255, 255, 255)
    thickness = 2
    
    max_x, min_x = float('-inf'), float('inf')
    max_y, min_y = float('-inf'), float('inf')
    
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
    
    box_max_x, box_min_x = int(max_x * image.shape[1]) + 10, int(min_x * image.shape[1]) - 10
    box_max_y, box_min_y = int(max_y * image.shape[0]) + 10, int(min_y * image.shape[0]) - 10
    
    top_left = (box_min_x, box_max_y)
    bottom_right = (box_max_x, box_min_y)
    
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
        #print(type(results))
    
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
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style()
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
                
                color = (255, 255, 255)
                thickness = -1
                radius = 5
                
                # landmark1 = face_landmarks.landmark[RIGHT_EYE_INDICES[3]]
                # landmark2 = face_landmarks.landmark[RIGHT_EYE_INDICES[10]]
                
                # center1_x, center1_y = int(landmark1.x * image.shape[1]), int(landmark1.y*image.shape[0])
                # center1 = (center1_x, center1_y)
                
                # center2_x, center2_y = int(landmark2.x * image.shape[1]), int(landmark2.y*image.shape[0])
                # center2 = (center2_x, center2_y)
                
                # cv2.circle(image, center1, radius, color, thickness)
                # cv2.circle(image, center2, radius, color, thickness)
                
                #left eye top indices: 0, 15, 14
                #left eye bottom indices: 7, 8, 10
                #left eye horizontal indices: 1, 4
                
                #right eye top indices: 1, 2, 3
                #right eye bottom indices: 13, 11, 10
                #right eye horizontal indices: 7, 6
                
                x1, y1 = face_landmarks.landmark[LEFT_EYE_INDICES[0]].x, face_landmarks.landmark[LEFT_EYE_INDICES[0]].y
                x2, y2 = face_landmarks.landmark[LEFT_EYE_INDICES[7]].x, face_landmarks.landmark[LEFT_EYE_INDICES[7]].y
                a = (x1, y1)
                b = (x2, y2)
                v1 = distance.euclidean(a, b)
                
                x3, y3 = face_landmarks.landmark[LEFT_EYE_INDICES[15]].x, face_landmarks.landmark[LEFT_EYE_INDICES[15]].y
                x4, y4 = face_landmarks.landmark[LEFT_EYE_INDICES[8]].x, face_landmarks.landmark[LEFT_EYE_INDICES[8]].y
                c = (x3, y3)
                d = (x4, y4)
                v2 = distance.euclidean(c, d)
                
                x5, y5 = face_landmarks.landmark[LEFT_EYE_INDICES[14]].x, face_landmarks.landmark[LEFT_EYE_INDICES[14]].y
                x6, y6 = face_landmarks.landmark[LEFT_EYE_INDICES[10]].x, face_landmarks.landmark[LEFT_EYE_INDICES[10]].y
                e = (x5, y5)
                f = (x6, y6)
                v3 = distance.euclidean(e, f)
                
                x7, y7 = face_landmarks.landmark[LEFT_EYE_INDICES[1]].x, face_landmarks.landmark[LEFT_EYE_INDICES[1]].y
                x8, y8 = face_landmarks.landmark[LEFT_EYE_INDICES[4]].x, face_landmarks.landmark[LEFT_EYE_INDICES[4]].y
                g = (x7, y7)
                h = (x8, y8)
                v4 = distance.euclidean(g, h)
                
                ear = (v1+v2+v3) / (3.0 * v4)
                
                threshold = 0.09
                if ear < threshold:
                    print("left eye is closed")
                else:
                    print("left eye is open")
                
                # Draw eye boxes
                draw_eye_box(image, LEFT_EYE_INDICES, face_landmarks)
                draw_eye_box(image, RIGHT_EYE_INDICES, face_landmarks)
                
            cv2.imshow('MediaPipe Face Mesh', image)
            if cv2.waitKey(5) & 0xFF == 27:
                cv2.destroyAllWindows()
                break
        else:
            print("No faces detected.")
            break
cap.release()