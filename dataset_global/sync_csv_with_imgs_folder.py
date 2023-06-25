import csv
import os
import shutil

csv_path = os.path.join('output', 'speedbumps.csv')
imgs_path = os.path.join('output', 'imgs')
imgs = os.listdir(imgs_path)
with open(csv_path) as f:
    all_lines = csv.reader(f)

    samples = []
    for line in all_lines:
      samples.append(line[1][5:])

count=0
for img in imgs:
  if img not in samples:
    count+=1
    print(img)
    # os.remove(os.path.join(imgs_path, img))
  
print(f"images to delete: {count}")

count=0
for sample in samples:
  if sample not in imgs:
    count+=1
    print(sample)

print(f"images mising: {count}")
