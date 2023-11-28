import cv2
import numpy as np
import tensorflow as tf

WIDTH = 320
HEIGHT = 320

# TensorFlow Lite 모델 로드
model_path = "/home/pi4/Capstone/Driver_Cam/drowsiness.tflite"
# model_path = "/home/pi4/Capstone/Driver_Cam/drowsiness_m.tflite"
interpreter = tf.lite.Interpreter(model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def detect_drowsiness(input_image):
    # 이미지 전처리
    input_image = np.expand_dims(input_image, axis=0)

    # 모델 추론
    interpreter.set_tensor(input_details[0]['index'], input_image.astype(np.float32))
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    result = output_data[0].astype(np.int32)
    print(result)

    return input_image
