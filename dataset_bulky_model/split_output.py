import os
import shutil
import math
from tqdm import tqdm
import csv

SPEED_BUMP_THRESHOLD=19
TRAIN_AMOUNT=.8
TEST_AMOUNT=.1
VAL_AMOUNT=.1

def split(out_path):

    out_path_split = os.path.join(out_path, "splitted_output")

    if os.path.isdir(out_path_split):
        shutil.rmtree(out_path_split) 

    os.makedirs(out_path_split)
    os.makedirs(os.path.join(out_path, "splitted_output/imgs"))

    speed_bumps_csv = open('output/splitted_output/speedbumps.csv', 'w')
    writer = csv.writer(speed_bumps_csv)

    total_samples = len(os.listdir(os.path.join(out_path, "imgs")))
    train_amount_spec = math.floor(TRAIN_AMOUNT*total_samples)
    test_amount_spec = math.floor(TEST_AMOUNT*total_samples)

    train_amount = 0
    test_amount = 0
    
    i=0
    previous_sample=""  
    previous_sample_type=""
    with open('output/multiclass.csv') as f:
        reader_obj = csv.reader(f)
        for row in tqdm(reader_obj, desc="Allocating on Train/Test/Validation"):
            
            if i<train_amount_spec:
                sample_type = "TRAIN"
            elif i<train_amount_spec+test_amount_spec:
                sample_type = "TEST"
            else:
                sample_type = "VALIDATION"

            if previous_sample == row[0].replace(f'{out_path}/','') and previous_sample_type != sample_type:
                sample_type = previous_sample_type

            previous_sample_type = sample_type
            data = [sample_type]+row
            
            if (int)(data[2])<=SPEED_BUMP_THRESHOLD: 
                data[2] = "SpeedBumpSign"
                out_path_split_img = f"{out_path_split}/{data[1].replace(f'{out_path}','')}"
                
                if not os.path.isfile(out_path_split_img): 
                    shutil.copyfile(data[1],out_path_split_img)
                
                data[1] = data[1].replace(f'{out_path}/', '')
                writer.writerow(data)
            else: continue
            
            if not previous_sample==data[1]:
                previous_sample=data[1]
                i+=1

                if i<train_amount_spec:
                    train_amount+=1
                elif i<train_amount_spec+test_amount_spec:
                    test_amount+=1

    print(f"TOTAL SAMPLES: {i}")
    print(f"Train: {train_amount}")
    print(f"Test: {test_amount}")
    print(f"Validation: {i-train_amount-test_amount}")

    speed_bumps_csv.close()

if __name__ == '__main__':
  split("output")