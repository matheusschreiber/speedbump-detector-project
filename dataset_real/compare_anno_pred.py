import json
import os
import cv2

with open('anno_coco.json') as json_file:
    anno_boxes = json.load(json_file)

with open('pred_coco.json') as json_file:
    pred_boxes = json.load(json_file)

for image in anno_boxes['images']:
    image_path = os.path.join('images', image['file_name'])

    img1 = cv2.imread(image_path)

    img2 = cv2.imread(image_path)

    for annotation in anno_boxes['annotations']:
        if annotation['image_id'] == image['id']:
            print(f"annot: {annotation['bbox']}")
            xmin = annotation['bbox'][0]
            ymin = annotation['bbox'][1]
            xmax = annotation['bbox'][0] + annotation['bbox'][2]
            ymax = annotation['bbox'][1] + annotation['bbox'][3]
            cv2.rectangle(img1, (xmin, ymin), (xmax, ymax), (0, 255, 0), 8)

    for prediction in pred_boxes:
        if prediction['image_id'] == image['id']:
            print(f"pred: {prediction['bbox']}")
            xmin = prediction['bbox'][0]
            ymin = prediction['bbox'][1]
            xmax = prediction['bbox'][0] + prediction['bbox'][2]
            ymax = prediction['bbox'][1] + prediction['bbox'][3]
            # cv2.rectangle(img2, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)
            cv2.rectangle(img1, (xmin, ymin), (xmax, ymax), (0, 0, 255), 5)

    # img1 = cv2.resize(img1, (320, 320))
    # img2 = cv2.resize(img2, (320, 320))

    img1 = cv2.resize(img1, (640, 640))
    # img2 = cv2.resize(img2, (640, 640))
    cv2.imshow('(annotation)-'+image_path+'1', img1)
    # cv2.imshow('(pred)-'+image_path+'2', img2)

    wait_time = 1000
    # while cv2.getWindowProperty('(annotation)-'+image_path+'1', cv2.WND_PROP_VISIBLE) and cv2.getWindowProperty('(pred)-'+image_path+'2', cv2.WND_PROP_VISIBLE) >= 1:
    while cv2.getWindowProperty('(annotation)-'+image_path+'1', cv2.WND_PROP_VISIBLE) >= 1:
        keyCode = cv2.waitKey(wait_time)
        if (keyCode & 0xFF) == ord("q"):
            cv2.destroyAllWindows()
            break
