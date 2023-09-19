import tensorflow as tf
import cv2

model = tf.keras.models.load_model('drowsiness.h5')
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    predictions = model.predict(image)
    print(predictions)

    cv2.imshow("ML test", image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()