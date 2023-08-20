import tensorflow as tf
import time
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import matplotlib.pyplot as plt
import json
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from math import floor
import csv
import cv2
from tqdm import tqdm
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

IMAGE_SIZE = (8, 8)

#PATH_TO_SAVED_MODEL="/home/matheus/Documentos/big-model/data/inference_graph/saved_model"
PATH_TO_SAVED_MODEL=os.path.join('inference_graph','saved_model')

#PATH_TO_LABEL_MAP="/home/matheus/Documentos/big-model/data/label_map.pbtxt"
PATH_TO_LABEL_MAP=os.path.join('label_map.pbtxt')

#PATH_TO_TEST_LABELS="/home/matheus/Documentos/big-model/data/test_labels.csv"
PATH_TO_TEST_LABELS=os.path.join('test_labels.csv')

#PATH_TO_IMAGES="/home/matheus/Documentos/big-model/data/images"
PATH_TO_IMAGES=os.path.join('images')

THRESHOLD_VALUE_CONFIDENCE=0.1


def convert_files_to_csv():
    def xml_to_csv(path):
      classes_names = []
      xml_list = []

      for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
          classes_names.append(member[0].text)
          value = (root.find('filename').text  ,
                   int(root.find('size')[0].text),
                   int(root.find('size')[1].text),
                   member[0].text,
                   int(member[5][0].text),
                   int(member[5][1].text),
                   int(member[5][2].text),
                   int(member[5][3].text))
          xml_list.append(value)
      column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
      xml_df = pd.DataFrame(xml_list, columns=column_name)
      classes_names = list(set(classes_names))
      classes_names.sort()
      return xml_df, classes_names

    for label_path in ['train_labels', 'test_labels']:
      image_path = os.path.join(os.getcwd(), label_path)
      xml_df, classes = xml_to_csv(label_path)
      xml_df.to_csv(f'{label_path}.csv', index=None)
      print(f'Successfully converted {label_path} xml to csv.')

    label_map_path = os.path.join("label_map.pbtxt")
    pbtxt_content = ""

    for i, class_name in enumerate(classes):
        pbtxt_content = (
            pbtxt_content
            + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(i + 1, class_name)
        )
    pbtxt_content = pbtxt_content.strip()
    with open(label_map_path, "w") as f:
        f.write(pbtxt_content)
        print('Successfully created label_map.pbtxt ')

def evaluate():
    detect_fn=tf.saved_model.load(PATH_TO_SAVED_MODEL)
    category_index=label_map_util.create_category_index_from_labelmap(PATH_TO_LABEL_MAP,use_display_name=True)

    def load_image_into_numpy_array(path):
        return np.array(Image.open(path))

    def infer(image_path):
      image_np = load_image_into_numpy_array(image_path)
      input_tensor = tf.convert_to_tensor(image_np)
      input_tensor = input_tensor[tf.newaxis, ...]

      detections = detect_fn(input_tensor)
      num_detections = int(detections.pop('num_detections'))
      detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
      detections['num_detections'] = num_detections
      detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

      bboxes_single_image = []
      for i, detection in enumerate(detections['detection_boxes']):
        if (detections['detection_scores'][i] > THRESHOLD_VALUE_CONFIDENCE):
          ymin = detection[0]
          xmin = detection[1]
          ymax = detection[2]
          xmax = detection[3]

          ymin = int(ymin * image_np.shape[0])
          xmin = int(xmin * image_np.shape[1])
          ymax = int(ymax * image_np.shape[0])
          xmax = int(xmax * image_np.shape[1])

          bboxes_single_image.append([xmin, ymin, xmax, ymax, detections['detection_scores'][i]])

      image_np_with_detections = image_np.copy()


      # viz_utils.visualize_boxes_and_labels_on_image_array(
      #       image_np_with_detections,
      #       detections['detection_boxes'],
      #       detections['detection_classes'],
      #       detections['detection_scores'],
      #       category_index,
      #       use_normalized_coordinates=True,
      #       max_boxes_to_draw=200,
      #       min_score_thresh=THRESHOLD_VALUE_CONFIDENCE,
      #       agnostic_mode=False)
      # %matplotlib inline
      # plt.figure(figsize=IMAGE_SIZE, dpi=200)
      # plt.axis("off")
      # plt.imshow(image_np_with_detections)
      # plt.show()

      return bboxes_single_image

    # infer('/home/matheus/Documentos/big-model/data/images/00011_COCO_train2014_000000137767.jpg')

    pred_bboxes = []
    anno_bboxes = []
    images = []

    row_count = 0

    with open(PATH_TO_TEST_LABELS, 'r') as f:
      row_count = sum(1 for line in f)

    progress_bar = tqdm(total=row_count)

    with open(PATH_TO_TEST_LABELS, 'r') as file:
      csvreader = csv.reader(file)
      last_sample=""
      gt_single_image=[]
      i=0

      for index,row in enumerate(csvreader):
        if index==0: continue

        xmin = int((float)(row[4]))
        ymin = int((float)(row[5]))
        xmax = int((float)(row[6]))
        ymax = int((float)(row[7]))

        if (last_sample==row[0]):
          gt_single_image.append([xmin, ymin, xmax, ymax])
        else:
          i+=1
          images.append({
              "id":i,
              "file_name":row[0],
              "width":row[1],
              "height":row[2]
            })
          last_sample=row[0]
          if gt_single_image: anno_bboxes.append(gt_single_image)
          pred_bboxes.append(infer(f"{PATH_TO_IMAGES}/{row[0]}"))
          gt_single_image=[]
          gt_single_image.append([xmin, ymin, xmax, ymax])

        progress_bar.update(1)



    def round_special(f: float):
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


if __name__ == "__main__":
    convert_files_to_csv()
    evaluate()
