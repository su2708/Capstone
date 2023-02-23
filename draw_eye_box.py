import cv2

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