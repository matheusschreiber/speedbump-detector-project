from PIL import Image
from tqdm import tqdm
import cv2
import os
import shutil

X_MIN=640
Y_MIN=640
LIMIT_TO_RESIZE=200

def reportImages():
  all_img_names = os.listdir("bgs/")
  file = open('shapes.txt','w')
  shapes=[]
  for name in tqdm(all_img_names, desc="Generating report"):
    im = cv2.imread(f'bgs/{name}')
    file.write((str)(im.shape) + " " + name + "\n") 
    shapes.append(im.shape)
  file.close()

  # print(*shapes, sep='\n')
  print(f"Ideal shape: ({min(shapes, key = lambda t: t[0])[0]}, {min(shapes, key = lambda t: t[1])[1]})")

def scaleImages():
  all_img_names = os.listdir("raw_bgs/")

  for name in tqdm(all_img_names, desc="Scaling images"):
    im = cv2.imread(f'raw_bgs/{name}')
    
    # if img is bigger than quota on both dimensions
    if (im.shape[0]>X_MIN and im.shape[1]>Y_MIN): 
      
      # if its landscape
      if (im.shape[0]>im.shape[1]):
        scaleFactor = (int)((X_MIN/im.shape[0]) * im.shape[1])
        Image.open(f"raw_bgs/{name}").resize((scaleFactor, X_MIN)).save(f"bgs/{name}")  
      
      # if its portrait
      else:
        scaleFactor = (int)((Y_MIN/im.shape[1]) * im.shape[0])
        Image.open(f"raw_bgs/{name}").resize((Y_MIN, scaleFactor)).save(f"bgs/{name}")  
      print(name)
      break

    else:
      # if its too tiny to use, discart it
      if (abs(X_MIN-im.shape[0])>LIMIT_TO_RESIZE or abs(Y_MIN-im.shape[1])>LIMIT_TO_RESIZE): 
        continue
      
      # if is short on width
      elif (im.shape[0]<im.shape[1]):
        scaleFactor = (int)((X_MIN/im.shape[0]) * im.shape[1])
        Image.open(f"raw_bgs/{name}").resize((scaleFactor, X_MIN)).save(f"bgs/{name}")
      
      # of os short on height
      else:
        scaleFactor = (int)((Y_MIN/im.shape[1]) * im.shape[0])
        Image.open(f"raw_bgs/{name}").resize((Y_MIN, scaleFactor)).save(f"bgs/{name}")


if __name__ == '__main__':
  # reportImages()
  scaleImages()