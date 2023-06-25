from coco_dataset import coco_dataset_download as coco
from tqdm import tqdm

classes = [
# 'dog', 'cat', 'person', 
# 'bird', 
# 'banana', 'sandwich',
# 'carrot', 'orange', 'apple', 'pizza', 'hot dog', 
# 'donut', 'cake', 'chair', 'dining table',
#  'toilet', 'bed', 
 'couch', 'keyboard','potted plant'
 'tv', 'remote', 'cell phone', 
 'microwave', 'toaster', 'refrigerator',
 'airplane', 'backpack', 'umbrella', 'tie'
 'suitcase', 'handbag', 'fire hydrant'
]

for cl in tqdm(classes):
  coco.coco_dataset_download(cl,3500,'./annotations/instances_train2014.json')