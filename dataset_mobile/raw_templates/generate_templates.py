import glob
import os
from PIL import Image
from tqdm import tqdm
import shutil
import argparse

def png_to_ppm(input_file, output_file):
    with Image.open(input_file) as img:
        img.save(output_file, "PPM")
    os.remove(input_file)


def change_black_tone(input_path, output_path):
  with Image.open(input_path) as img:
    img = img.convert('RGBA')
    pixels = img.load()
    for i in range(img.size[0]):
      for j in range(img.size[1]):
        color = pixels[i, j]
        if color[3] > 0 and color[0] < 10 and color[1] < 10 and color[2] < 10:
          pixels[i, j] = (30, 30, 30, color[3]) 
    img.save(output_path)

def parse_args():
  parser = argparse.ArgumentParser(
    description='Generate a template set.')

  parser.add_argument('--out-path', dest='out_path', type=str, required=True, help='Output path to the .ppm templates')

  return parser.parse_args()

if __name__ == '__main__':

  args = parse_args()

  if os.path.isdir(args.out_path): shutil.rmtree(args.out_path)
  os.makedirs(args.out_path)

  for i in tqdm(glob.glob("png/*")):
    image_file = i.split('/')[1]
    change_black_tone(i, f"../templates/{image_file}")
    png_to_ppm(f"../templates/{image_file}", f"../templates/{image_file.split('.')[0]}.ppm")



