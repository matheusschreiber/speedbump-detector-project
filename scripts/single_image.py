import tensorflow as tf
assert tf.__version__.startswith('2')
import numpy as np
import cv2
from tqdm import tqdm

THRESHOLD_VALUE_CONFIDENCE=0.1

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def join_results(raw_results, img_height, img_width, section_height, section_width):
  idx = 0

  output_detection = []

  print(f"raw_results:{raw_results}")

  for y in range(0, img_height, section_height):
    for x in range(0, img_width, section_width):
      if x+section_width > img_width or y+section_height>img_height: print("nao deve acontecer")

      bboxes = raw_results[idx][0][1]
      for i, bbox in enumerate(bboxes):
        ymin = round((bbox[0] * section_height + y)/img_height, 4)
        xmin = round((bbox[1] * section_width + x)/img_width, 4)
        ymax = round((bbox[2] * section_height + y)/img_height, 4)
        xmax = round((bbox[3] * section_width + x)/img_width, 4)
        
        score = raw_results[idx][0][0][i]
        output_detection.append([ymin, xmin, ymax, xmax, score])
      
      output_detection.append([
        round((0 * section_height + y)/img_height, 4),
        round((0 * section_width + x)/img_width, 4),
        round((1 * section_height + y)/img_height, 4),
        round((1 * section_width + x)/img_width, 4),
        -1
      ])
      idx+=1

  output_detection.sort(key=lambda x: x[4], reverse=True)
  print(f"output_detection: {output_detection[0]}")
  output_detection.append([0,0,1,1,-1])
  return output_detection

def big_images_infer(image_path):
  raw_image = cv2.imread(image_path)
  height, width, _ = raw_image.shape

  if width % 640!=0 or height % 640!=0: 
    image = cv2.copyMakeBorder(raw_image, 0, 640-(height % 640), 0, 640-(width % 640), cv2.BORDER_CONSTANT, value=(0,0,0))
  else:
    image = raw_image

  height, width, _ = image.shape
  sections = []
  section_height = 640
  section_width = 640
  
  for y in range(0, height, section_height):
    for x in range(0, width, section_width):
      if x+section_width > width or y+section_height>height: continue
      section = image[y:y + section_height, x:x + section_width]
      sections.append(section)

  all_results = []
  for section in tqdm(sections):
    detection_results = []
    section_resized = cv2.resize(section, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    section_blueprinted = cv2.cvtColor(section_resized, cv2.COLOR_BGR2RGB)
    section_tensor = tf.convert_to_tensor(section_blueprinted, dtype=tf.uint8)
    section_np = np.expand_dims(section_tensor, axis=0).astype(input_details[0]['dtype'])
    interpreter.set_tensor(input_details[0]['index'], section_np)
    interpreter.invoke()
    section_scores = interpreter.get_tensor(output_details[0]['index'])[0]
    section_boxes = interpreter.get_tensor(output_details[1]['index'])[0]
    detection_results.append((section_scores, section_boxes))
    all_results.append(detection_results)
  
  results = join_results(all_results, height, width, section_height, section_width)
  scaled_annotations = []
  scaled_image_to_annotate = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))

  for bbox in results: 
    ymin_annotation = int(bbox[0] * scaled_image_to_annotate.shape[0])
    xmin_annotation = int(bbox[1] * scaled_image_to_annotate.shape[1])
    ymax_annotation = int(bbox[2] * scaled_image_to_annotate.shape[0])
    xmax_annotation = int(bbox[3] * scaled_image_to_annotate.shape[1])
    scaled_annotations.append([xmin_annotation, ymin_annotation, xmax_annotation, ymax_annotation, bbox[4]])

    ymin = bbox[0] * image.shape[0]
    xmin = bbox[1] * image.shape[1]
    ymax = bbox[2] * image.shape[0]
    xmax = bbox[3] * image.shape[1]

    if (bbox[4]>THRESHOLD_VALUE_CONFIDENCE):
      cv2.rectangle(image, ((int)(xmin), (int)(ymin)), ((int)(xmax), (int)(ymax)), (0, 255, 0), 2)
    elif (bbox[4]<0):
      cv2.rectangle(image, ((int)(xmin), (int)(ymin)), ((int)(xmax), (int)(ymax)), (255, 0, 0), 2)
    # else:
    #   cv2.rectangle(image, ((int)(xmin), (int)(ymin)), ((int)(xmax), (int)(ymax)), (0, 255, 255), 2)

  print(f"scaled_annotations: {scaled_annotations[0]}")
  image_to_display = cv2.resize(image, (1000, 500))
  cv2.imshow('SpeedBumpDetection', image_to_display)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def infer(image_path):
  image = cv2.imread(image_path)

  if abs(image.shape[0] - image.shape[1]) > 1000:
    big_images_infer(image_path)
    return

  image_resized = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
  image_blueprinted = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
  image_tensor = tf.convert_to_tensor(image_blueprinted, dtype=tf.uint8)
  image_np = np.expand_dims(image_tensor, axis=0).astype(input_details[0]['dtype'])
  interpreter.set_tensor(input_details[0]['index'], image_np)
  interpreter.invoke()

  output_scores = interpreter.get_tensor(output_details[0]['index'])[0]
  output_boxes = interpreter.get_tensor(output_details[1]['index'])[0]
 
  for i in (range(len(output_boxes))): 
    ymin = output_boxes[i][0]
    xmin = output_boxes[i][1]
    ymax = output_boxes[i][2]
    xmax = output_boxes[i][3]

    ymin = int(ymin * image_resized.shape[0])
    xmin = int(xmin * image_resized.shape[1])
    ymax = int(ymax * image_resized.shape[0])
    xmax = int(xmax * image_resized.shape[1])

    THRESHOLD_VALUE_CONFIDENCE=0.1

    if (output_scores[i]>THRESHOLD_VALUE_CONFIDENCE):
      cv2.rectangle(image_resized, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    else:
      cv2.rectangle(image_resized, (xmin, ymin), (xmax, ymax), (0, 255, 255), 2)
  
  cv2.imshow('SpeedBumpDetection', image_resized)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
    
# infer("imgs/3e_LqA8g6OAJI0jqMm30Vg.jpg")
# infer("imgs/-zH_fa05bGgBWvlSrjGSzg.jpg")
# infer("imgs/CP3XbDvccwG10RbwposT_w.jpg")
infer("imgs/IW7Xuhq_ywISaV8DSaTYBQ.jpg")


