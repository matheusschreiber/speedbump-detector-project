import glob
import os
from PIL import Image

def png_to_ppm(input_file, output_file):
    with Image.open(input_file) as img:
        img.save(output_file, "PPM")
    os.remove(input_file)

for i in glob.glob("ppm/*"):
    png_to_ppm(i, f"ppm/{i.split('/')[1].split('.')[0]}.ppm")
    print(f"{i} => {i.split('/')[1]}.ppm")


