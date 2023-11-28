from scipy.spatial import distance

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

def get_EAR(eye_indices, landmarks, side):
    if side == "left":
        eye_top = L_eye_top
        eye_bottom = L_eye_bottom
        eye_width = L_eye_width
    else:
        eye_top = R_eye_top
        eye_bottom = R_eye_bottom
        eye_width = R_eye_width
    
    # get average height of eye
    eye_top_coordinates = []
    for i, idx in enumerate(eye_top):
        x, y = landmarks.landmark[eye_indices[idx]].x, landmarks.landmark[eye_indices[idx]].y
        eye_top_coordinates.append((x, y))
        
    eye_bottom_coordinates = []
    for i, idx in enumerate(eye_bottom):
        x, y = landmarks.landmark[eye_indices[idx]].x, landmarks.landmark[eye_indices[idx]].y
        eye_bottom_coordinates.append((x, y))
    
    eye_height_avg = float(0.0)
    for i in range(len(eye_top_coordinates)):
        d = distance.euclidean(eye_top_coordinates[i], eye_bottom_coordinates[i])
        eye_height_avg += d
    
    eye_height_avg = eye_height_avg / 3.0
    
    # get width of eye
    eye_width_coordinates = []
    for i, idx in enumerate(eye_width):
        x, y = landmarks.landmark[eye_indices[idx]].x, landmarks.landmark[eye_indices[idx]].y
        eye_width_coordinates.append((x, y))
        
    eye_width = distance.euclidean(eye_width_coordinates[0], eye_width_coordinates[1])
    
    # EAR(Eye Aspect Ratio) = the average heights of eye / the width of eye
    ear = eye_height_avg / eye_width

    threshold = 0.15
    eye_status = 0 if ear < threshold else 1
    
    return eye_status
