from coco_dataset import coco_dataset_download as coco
from tqdm import tqdm

classes = [
'dog', 'cat', 'person', 'bird', 'banana', 'sandwich',
'carrot', 'orange', 'apple', 'pizza', 'hot dog', 
'donut', 'cake', 'chair', 'dining table', 'toilet', 
'bed', 'couch'
]

for cl in tqdm(classes):
  coco.coco_dataset_download(cl,600,'./annotations/instances_train2014.json')