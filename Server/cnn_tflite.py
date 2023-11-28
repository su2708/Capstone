import cv2
import numpy as np
import tensorflow as tf

# TensorFlow Lite 모델 로드
interpreter = tf.lite.Interpreter(model_path="CNNmodel_slr.tflite")
interpreter.allocate_tensors()

# 모델 입력 및 출력 텐서 가져오기
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

class_names = ['not curve', 'right', 'left']

def curve(roi):
    input_frame = cv2.resize(roi, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    
    input_data = np.expand_dims(input_frame, axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_data.astype(np.float32))
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = class_names[np.argmax(output_data)]
    
    return predicted_class
