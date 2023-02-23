from scipy.spatial import distance

def get_ear_status(eye_indices, eye_top, eye_bottom, eye_width, landmarks):    
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