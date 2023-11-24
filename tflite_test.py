import cv2
import numpy as np
import tensorflow as tf

# TensorFlow Lite 모델 로드
interpreter = tf.lite.Interpreter(model_path="Driver_Cam/drowsiness.tflite")
interpreter.allocate_tensors()

# 모델 입력 및 출력 텐서 가져오기
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 웹캠에서 영상 가져오기
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 프레임 크기 변경 (모델 입력 크기와 일치하도록)
    resized_frame = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))

    # 모델 입력 데이터 전처리
    input_data = np.expand_dims(resized_frame, axis=0)
    input_data = input_data.astype(np.float32) / 255.0  # 정규화

    # 모델 실행
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # 모델 출력 얻기
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # 출력을 이용한 눈 감김 감지 로직 추가
    # 예를 들어, output_data를 분석하여 눈 감김 여부를 판단

    # 결과 시각화
    cv2.imshow('Drowsiness Detection', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# 웹캠 해제 및 OpenCV 창 닫기
cap.release()
cv2.destroyAllWindows()