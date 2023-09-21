import tensorflow as tf
import cv2

print('hello')

# 모델 파일('drowsiness.h5') 경로 지정 (문자열로)
model_path = './drowsiness.h5'

# 'drowsiness.h5' 파일을 로드
model = tf.keras.models.load_model(model_path)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_size = (80, 80)
    image = image = tf.image.resize(image, input_size)
    image = image / 255.0
    image = tf.expand_dims(image, axis=0)

    predictions = model.predict(image)
    print(predictions)

    cv2.imshow("ML test", image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()