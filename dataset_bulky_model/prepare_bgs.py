from PIL import Image
from tqdm import tqdm
import cv2
import os
import shutil

DIM = 640
LIMIT = 200
OUTPUT_PATH = "bgs"
INPUT_PATH = "raw_bgs"

def prepare_bgs():
  if os.path.isdir(OUTPUT_PATH): shutil.rmtree(OUTPUT_PATH)
  os.makedirs(OUTPUT_PATH)
  
  all_img_names = os.listdir(INPUT_PATH)
    
  for name in tqdm(all_img_names):
    image = cv2.imread(os.path.join(INPUT_PATH, name))
    
    # discarting low quality images
    if image.shape[0] < LIMIT or image.shape[1] < LIMIT: continue
  
    # calculation scale factor based on smaller dimension
    scale_factor = DIM/min(image.shape[0], image.shape[1])
    image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

    # cropping scaled image
    image_width_middle = int(image.shape[1]/2)
    image_height_middle = int(image.shape[0]/2)
    frame = int(DIM/2)
    image = image[image_height_middle-frame:image_height_middle+frame, image_width_middle-frame:image_width_middle+frame]
    image = cv2.resize(image, (DIM,DIM))

    # debug
    # cv2.imshow(f"{name}_({image.shape[0]},{image.shape[1]})", image)
    # cv2.waitKey()

    cv2.imwrite(os.path.join(OUTPUT_PATH, name), image)

if __name__ == '__main__':
  prepare_bgs()