import os
import glob
import argparse
import shutil
from tqdm import tqdm

def verify_directory(path):
  if os.path.isdir(path): shutil.rmtree(path)
  
  os.makedirs(path)
  os.makedirs(f'{path}/imgs')


def parse_args():
  parser = argparse.ArgumentParser(
    description='Merge annotations with images on csv.')

  parser.add_argument('--input-path', dest='in_path', type=str, required=True, help='Directory where images and annotations are located')
  parser.add_argument('--out-path', dest='out_path', type=str, required=True, help='Output path to the set')

  return parser.parse_args()

if __name__ == '__main__':

  args = parse_args()
  verify_directory(args.out_path)

  search_string = f"{args.in_path}/*.txt"
  csv_lines = []

  for i in glob.glob(search_string):
    file_name = i.replace(f'{args.in_path}/', '')
    with open(i, "r") as file:
      lines = file.read().split('\n')
      for line in lines:
        coords = line.split(' ')
        coords.pop(0)
        if coords: 
          image_name = file_name.replace('.txt','.jpg')
          csv_lines.append(f"TEST,imgs/{image_name},SpeedBumpSign,{(float)(coords[0]):.4f},{(float)(coords[1]):.4f},,,{(float)(coords[2]):.4f},{(float)(coords[3]):.4f},,")
          
          out_image = f'{args.out_path}/imgs/{image_name}'
          in_image = f'{args.in_path}/{image_name}'
          
          if not os.path.isfile(out_image): 
            shutil.copyfile(in_image, out_image)

  
  with open(os.path.join(args.out_path, "speedbumps.csv"), "w") as csv_file:
    csv_file.write("\n".join(csv_lines) + "\n")
    
        
