import tensorflow as tf
assert tf.__version__.startswith('2')
import numpy as np
import cv2

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('test.mp4')


interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()


input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()



while(True):
    ret, frame = cap.read()

    image_resized = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    image_blueprinted = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    image_tensor = tf.convert_to_tensor(image_blueprinted, dtype=tf.uint8)
    image_np = np.expand_dims(image_tensor, axis=0).astype(input_details[0]['dtype'])
    interpreter.set_tensor(input_details[0]['index'], image_np)
    interpreter.invoke()

    output_scores = interpreter.get_tensor(output_details[0]['index'])[0]
    output_boxes = interpreter.get_tensor(output_details[1]['index'])[0]
    print(output_scores)

#     cv2.imshow('frame',image_resized)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
