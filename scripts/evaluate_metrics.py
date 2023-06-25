import numpy as np
import tensorflow as tf
assert tf.__version__.startswith('2')
import cv2
import csv
from tqdm import tqdm

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']

THRESHOLD_VALUE_CONFIDENCE=0.1

def join_results(raw_results, img_height, img_width, section_height, section_width):
  idx = 0

  output_detection = []

  for y in range(0, img_height, section_height):
    for x in range(0, img_width, section_width):
      if x+section_width > img_width or y+section_height>img_height: continue

      bboxes = raw_results[idx][0][1]
      for i, bbox in enumerate(bboxes):
        ymin = bbox[0] * section_height + y 
        xmin = bbox[1] * section_width + x 
        ymax = bbox[2] * section_height + y
        xmax = bbox[3] * section_width + x
        
        score = raw_results[idx][0][0][i]
        if score<THRESHOLD_VALUE_CONFIDENCE: continue
        output_detection.append([xmin, ymin, xmax, ymax, score])
      idx+=1
    
  output_detection.sort(key=lambda x: x[4], reverse=True)
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
  for section in enumerate(sections):
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
  return results

def infer(image_path):
  image = cv2.imread(image_path)

  if abs(image.shape[0] - image.shape[1]) > 500:
    return big_images_infer(image_path)

  image_resized = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
  image_blueprinted = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
  image_tensor = tf.convert_to_tensor(image_blueprinted, dtype=tf.uint8)
  image_np = np.expand_dims(image_tensor, axis=0).astype(input_details[0]['dtype'])
  interpreter.set_tensor(input_details[0]['index'], image_np)
  interpreter.invoke()

  output_scores = interpreter.get_tensor(output_details[0]['index'])[0]
  output_boxes = interpreter.get_tensor(output_details[1]['index'])[0]
  bboxes_single_image = []

  for i in (range(len(output_boxes))): 
    ymin = output_boxes[i][0]
    xmin = output_boxes[i][1]
    ymax = output_boxes[i][2]
    xmax = output_boxes[i][3]

    xmin = int(xmin * image_resized.shape[1])
    xmax = int(xmax * image_resized.shape[1])
    ymin = int(ymin * image_resized.shape[0])
    ymax = int(ymax * image_resized.shape[0])

    if (output_scores[i]>THRESHOLD_VALUE_CONFIDENCE):
      bboxes_single_image.append([xmin, ymin, xmax, ymax, output_scores[i]])
  return bboxes_single_image

pred_bboxes = []
anno_bboxes = []
images = []

with open("speedbumps.csv", 'r') as file:
  csvreader = csv.reader(file)
  last_sample=""
  gt_single_image=[]
  i=0
  for row in tqdm(csvreader):
    image = cv2.imread(row[1])
    image_resized = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    
    xmin = int((float)(row[3])*image_resized.shape[1])
    ymin = int((float)(row[4])*image_resized.shape[0])
    xmax = int((float)(row[7])*image_resized.shape[1])
    ymax = int((float)(row[8])*image_resized.shape[0])

    if (last_sample==row[1]):
      gt_single_image.append([xmin, ymin, xmax, ymax])
    else:
      i+=1
      images.append({
          "id":i,
          "file_name":row[1],
          "width":image_resized.shape[1],
          "height":image_resized.shape[0]
        })
      last_sample=row[1]
      if gt_single_image: anno_bboxes.append(gt_single_image)
      pred_bboxes.append(infer(row[1]))
      gt_single_image=[]
      gt_single_image.append([xmin, ymin, xmax, ymax])

  pred_bboxes.pop()
  images.pop()

print()
print(pred_bboxes)
print(anno_bboxes)