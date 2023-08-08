import numpy as np
import tensorflow as tf
assert tf.__version__.startswith('2')
import cv2
from tqdm import tqdm
import csv
import json
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

from math import floor


pred_bboxes = []
anno_bboxes = []
images = []
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']
THRESHOLD_VALUE_CONFIDENCE=0.1

def infer(image_path):
  image = cv2.imread(image_path)
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
      cv2.rectangle(image_resized, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    elif (output_scores[i]>THRESHOLD_VALUE_CONFIDENCE*.5):
      cv2.rectangle(image_resized, (xmin, ymin), (xmax, ymax), (0, 255, 255), 2)

  image_resized = cv2.resize(image_resized, (500,500))
  #cv2_imshow(image_resized)
  return bboxes_single_image



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
      #print(row[1])
      pred_bboxes.append(infer(row[1]))
      gt_single_image=[]
      gt_single_image.append([xmin, ymin, xmax, ymax])

  pred_bboxes.pop()
  images.pop()

#print()
#print(pred_bboxes)
#print(anno_bboxes)


def round_special(f: float):
  # print("number: ", f)
  # if f>=0.98: return 1.0
  # elif f>=0.9: return float(str(f)[:4])
  # else: return round(f.astype(float),2)
  return float(str(f)[:4])


pred_coco = []
anno_coco = []

imgs_coco = []
annotations = []

for idImg, annotations_on_image in enumerate(anno_bboxes):
  for idAnno, bbox in enumerate(annotations_on_image):
    annotations.append({
        "id":idAnno+idImg+1,
        "image_id":idImg+1,
        "category_id":1,
        "bbox":[bbox[0],bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]],
        "area": (bbox[2]-bbox[0])*(bbox[3]-bbox[1]),
        "iscrowd":0
    })

  for prediction in pred_bboxes[idImg]:

    pred_coco.append({
      "image_id": idImg+1,
      "category_id": 1,
      "bbox": [
          prediction[0],
          prediction[1],
          prediction[2]-prediction[0],
          prediction[3]-prediction[1],
      ],
      "score":round_special(prediction[4])
    })

    # print(round_special(prediction[4]))

anno_coco = {
    "images":images,
    "annotations": annotations,
    "categories":[
        {"id":1, "name":"speedbumpsign"}
    ]
}

#print(pred_coco)

#print()

#print(anno_coco)

with open('pred_coco.json', 'w') as fp:
    json.dump(pred_coco, fp)

with open('anno_coco.json', 'w') as fp:
    json.dump(anno_coco, fp)


annFile = 'anno_coco.json'
cocoGt = COCO(annFile)
predFile = 'pred_coco.json'
cocoDt = cocoGt.loadRes(predFile)
cocoEval = COCOeval(cocoGt, cocoDt, 'bbox')
cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize()
