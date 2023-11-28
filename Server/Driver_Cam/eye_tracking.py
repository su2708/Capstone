import cv2
import numpy as np

'''
0: 왼눈동자 안 - 469
1: 왼눈동자 위 - 470
2: 왼눈동자 밖 - 471
3: 왼눈동자 아래 - 472
4: 오른눈동자 밖 - 474
5: 오른눈동자 위 - 475
6: 오른눈동자 안 - 476
7: 오른눈동자 아래 - 477
'''

def track_eyes(image, face_landmarks, iris_indices):
    img_h, img_w, img_c = image.shape
    face_2d = []
    face_3d = []

    for idx, lm in enumerate(face_landmarks.landmark):
        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199 or idx == 471 or idx == 474:
            '''
            33: 왼쪽 눈 바깥
            263: 오른쪽 눈 바깥
            1: 코 끝
            61: 입술 왼쪽 끝
            291: 입술 오른쪽 끝
            199: 턱 끝
            '''
            if idx == 471:
                left_iris_2d = (lm.x * img_w, lm.y * img_h)
                left_iris_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
            elif idx == 474:
                right_iris_2d = (lm.x * img_w, lm.y * img_h)
                right_iris_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
            
            x, y = int(lm.x * img_w), int(lm.y * img_h)

            # Get the 2D Coordinates
            face_2d.append([x, y])

            # Get the 3D Coordinates
            face_3d.append([x, y, lm.z]) 
            
    # Convert it to the NumPy array
    face_2d = np.array(face_2d, dtype=np.float64)

    # Convert it to the NumPy array
    face_3d = np.array(face_3d, dtype=np.float64)

    # The camera matrix
    focal_length = 1 * img_w

    cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                            [0, focal_length, img_w / 2],
                            [0, 0, 1]])
    
    # The distortion parameters
    dist_matrix = np.zeros((4, 1), dtype=np.float64)

    # Solve PnP
    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

    # Get rotational matrix
    rmat, jac = cv2.Rodrigues(rot_vec)

    # Get angles
    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

    # Get the y rotation degree
    x = angles[0] * 360
    y = angles[1] * 360
    z = angles[2] * 360   

    # See where the user's head tilting
    if y < -10:
        text = "Looking Left"
    elif y > 10:
        text = "Looking Right"
    elif x < -10:
        text = "Looking Down"
    elif x > 10:
        text = "Looking Up"
    else:
        text = "Forward"

    # Display the iris direction
    left_iris_3d_projection, jacobian = cv2.projectPoints(left_iris_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
    right_iris_3d_projection, jacobian = cv2.projectPoints(right_iris_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

    p1 = (int(left_iris_2d[0]), int(left_iris_2d[1]))
    p2 = (int(left_iris_2d[0] + y * 10) , int(left_iris_2d[1] - x * 10))
    p3 = (int(right_iris_2d[0]), int(right_iris_2d[1]))
    p4 = (int(right_iris_2d[0] + y * 10), int(right_iris_2d[1] - x * 10))
    
    cv2.line(image, p1, p2, (255, 0, 0), 3)
    cv2.line(image, p3, p4, (0, 0, 255), 3)

    # Add the text on the image
    cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    cv2.putText(image, "x: " + str(np.round(x,2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, "y: " + str(np.round(y,2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, "z: " + str(np.round(z,2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    pass