import csv
import os
import shutil

csv_path = os.path.join('output', 'speedbumps.csv')
imgs_path = os.path.join('output', 'imgs')
imgs = os.listdir(imgs_path)

new_csv=[]

with open(csv_path) as f:
  all_lines = csv.reader(f)

  for line in all_lines:
    sample = line[1][5:]
    if sample not in imgs: continue
    new_csv.append(line)

with open(os.path.join('output','new_speedbumps.csv'),'w') as output_csv:
  for line in new_csv:
    string = ""
    for a in line:
        if string=="":string=a
        else: string=string+','+a      
    string+='\n'    
    output_csv.write(string)
