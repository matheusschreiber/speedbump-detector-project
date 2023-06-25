import json
import csv
import cv2
from tqdm import tqdm
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

THRESHOLD_TEST = 0.6

def round_special(f: float):
  return float(str(f)[:4])

def load_images():
  images = []
  with open("speedbumps.csv", 'r') as file:
    csvreader = csv.reader(file)
    last_sample=""
    i=0
    for row in tqdm(csvreader):
      image = cv2.imread(row[1])
      image_resized = cv2.resize(image, (320,320))
      
      if (not last_sample==row[1]):
        i+=1
        images.append({
            "id":i,
            "file_name":row[1],
            "width":image_resized.shape[1],
            "height":image_resized.shape[0]
          })
        last_sample=row[1]
  return images


annotations = open('annotations.json')
preductions = open('predictions.json')

anno_bboxes = json.load(annotations)
pred_bboxes = json.load(preductions)

annotations.close()
preductions.close()

aux_pred_bboxes = []
aux_anno_bboxes = []
for idx, sample in enumerate(pred_bboxes):
  aux_samples = []
  for bbox in sample:
    if bbox[4] >= THRESHOLD_TEST:
      aux_samples.append(bbox)
  
  if aux_samples:
    aux_pred_bboxes.append(aux_samples[:])
    aux_anno_bboxes.append(anno_bboxes[idx])
    

pred_bboxes = aux_pred_bboxes[:]
anno_bboxes = aux_anno_bboxes[:]

for i in pred_bboxes: print(i)
print()
for i in anno_bboxes: print(i)

annotations.close()
preductions.close()

pred_coco = []
anno_coco = []

imgs_coco = []
annotations = []

images = load_images()

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

anno_coco = {
    "images":images,
    "annotations": annotations,
    "categories":[
        {"id":1, "name":"speedbumpsign"}
    ]
}

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