# more info on output via https://cocodataset.org/#detection-eval
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

# load the ground truth annotations and predictions
annFile = 'anno_coco_test.json' # ground truth annotations
cocoGt = COCO(annFile)

predFile = 'pred_coco_test.json' # model predictions
cocoDt = cocoGt.loadRes(predFile)

# evaluate the model using COCOeval
cocoEval = COCOeval(cocoGt, cocoDt, 'bbox')
cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize()