import cv2
import numpy as np
import tensorflow as tf

WIDTH = 320
HEIGHT = 320

# TensorFlow Lite 모델 로드
model_path = "/home/pi4/Capstone/examples/lite/examples/object_detection/raspberry_pi/efficientdet_lite0.tflite"
interpreter = tf.lite.Interpreter(model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def detect_objects_in_image(input_image):

    # 이미지 전처리
    input_shape = input_details[0]['shape']
    input_image = cv2.resize(input_image, (input_shape[2], input_shape[1]))
    input_image = np.expand_dims(input_image, axis=0)

    # 모델 추론
    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # 결과 이미지 생성
    image = input_image[0].copy()
    detected_objects = output_data[0]
    for obj in detected_objects:
        confidence = obj[2]
        if confidence > 0.8:  # 신뢰도가 0.8 이상인 결과만 표시
            x1, y1, x2, y2 = map(int, obj[:4] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]]))
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            label = f"Object: {obj[1]}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    image = cv2.resize(image, (WIDTH, HEIGHT))
    print("blackbox done")
    return image
