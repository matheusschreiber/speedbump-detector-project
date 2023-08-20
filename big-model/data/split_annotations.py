import os
import shutil


annotations_dir = os.path.join('annotations')
i=0

if os.path.isdir('test_labels'): shutil.rmtree('test_labels')
if os.path.isdir('train_labels'): shutil.rmtree('train_labels')

os.makedirs('test_labels')
os.makedirs('train_labels')

num_samples = len(os.listdir(annotations_dir))

for annotation in os.listdir(annotations_dir):
    old_dir = os.path.join('annotations', annotation)
    if i>0.8*num_samples:
        new_dir = os.path.join('test_labels', annotation)
    else:
        new_dir = os.path.join('train_labels', annotation)

    shutil.move(old_dir, new_dir)
    i+=1
 
