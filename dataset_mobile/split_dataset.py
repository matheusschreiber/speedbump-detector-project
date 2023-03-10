import csv
import os
from math import floor
from tqdm import tqdm
import shutil

SPEED_BUMP_THRESHOLD=15
TRAIN_AMOUNT=.8
TEST_AMOUNT=.1
VAL_AMOUNT=.1

# FIXME: other signs images are beeing excluded

def split():
  out_path="output"
  out_path_split= os.path.join(out_path, "splitted_output")
  
  if os.path.isdir(out_path_split):
    shutil.rmtree(out_path_split) 
  
  os.makedirs(out_path_split)
  os.makedirs(os.path.join(out_path, "splitted_output/imgs"))

  speed_bumps_csv = open('output/splitted_output/speedbumps.csv', 'w')
  writer = csv.writer(speed_bumps_csv)

  total_samples = len(os.listdir(os.path.join(out_path, "imgs")))
  train_amount = floor(TRAIN_AMOUNT*total_samples)
  test_amount = floor(TEST_AMOUNT*total_samples)
  val_amount = total_samples-train_amount-test_amount
  i=0
  with open('output/multiclass.csv') as f:
    reader_obj = csv.reader(f)
    previous_sample=""  
    for row in tqdm(reader_obj, desc="Allocating on Train/Test/Validation"):
      
      if i<train_amount:
        data=["TRAINING"]
      elif i<train_amount+test_amount:
        data=["TEST"]
      else:
        data=["VALIDATION"]

      data = data+row
      if (int)(data[2])<=SPEED_BUMP_THRESHOLD: 
        data[2] = "SpeedBumpSign"
        out_path_split_img = f"{out_path_split}/{data[1].replace(f'{out_path}/','')}"

        if not os.path.isfile(out_path_split_img): 
          shutil.copyfile(data[1],out_path_split_img)

        data[1] = data[1].replace(f'{out_path}/', '')
        writer.writerow(data)
              
      if not previous_sample==data[1]:
        previous_sample=data[1]
        i+=1
  
  print(f"TOTAL SAMPLES: {total_samples}")
  print(f"Train: {train_amount}")
  print(f"Test: {test_amount}")
  print(f"Validation: {val_amount}")
  
  speed_bumps_csv.close()

if __name__ == '__main__':
  split()