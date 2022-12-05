import json
import os
import shutil

class Region:
  """
  name
  all_points_x
  all_points_y
  region_attributes
  """
  def __init__(self, name, all_points_x, all_points_y, region_attributes):
    self.name = name
    self.all_points_x = all_points_x
    self.all_points_y = all_points_y
    self.region_attributes = region_attributes


class Image:
  """
  fileref
  size
  filename
  base64_img_data
  file_attributes
  regions
  """
  def __init__(self, fileref, size, filename, base64_img_data, regions):
    self.fileref = fileref
    self.size = size
    self.filename = filename
    self.base64_img_data = base64_img_data
    self.regions = regions


if not os.path.isdir('./output'): 
  print("Could not find output folder")
  exit()

if not os.path.isdir('./output/imgs'): 
  print("Could not find imgs folder")
  exit()
if not os.path.isfile('./output/multiclass.csv'): 
  print("Could not find multiclass.csv")
  exit()
  

os.chdir('./output')

outputs = {
  "via_region_data_train":{},
  "via_region_data_val":{}
}

train = 140
total_images = len(os.listdir('./imgs'))
print(f'Generating {train} train images and {total_images - train} validation images')

count = 0
regions = {}
indx = 0

template_bump_limit = 6
print(f'Last speed bump template: {template_bump_limit}')

prev_image='00000_'

if os.path.isdir('sb_sign'):
  shutil.rmtree('sb_sign')

os.mkdir('./sb_sign')
os.mkdir('./sb_sign/train')
os.mkdir('./sb_sign/val')

with open('multiclass.csv', 'r') as f:
  data = f.readlines()

for image in data:
  image = image.split(',')
  image_name = image[0][12:]

  
  
  pointsX = []
  pointsY = []

  for coord in range(0, len(image[1:-1]), 2):
    pointsX.append((int)(image[coord+1]))

  for coord in range(1, len(image[1:-1]), 2):
    pointsY.append((int)(image[coord+1]))

  regClass = Region("polygon", pointsX, pointsY,"")

  if not (prev_image in image_name):
    regions = {}
    prev_image = image_name[:6]
    count+=1

  if not (int)(image[-1]) <= 6:
    continue

  if not regions:
    regions = {
      f"{indx}": {
        "shape_attributes":{
          "name":regClass.name,
          "all_points_x":regClass.all_points_x,
          "all_points_y":regClass.all_points_y,
        },"region_attributes": {}
      }
    }
  else:
    newRegion = {
      f"{indx}": {
        "shape_attributes":{
          "name":regClass.name,
          "all_points_x":regClass.all_points_x,
          "all_points_y":regClass.all_points_y,
        },"region_attributes": {}
        
      }
    }
    regions = dict(regions, **newRegion)
    
  indx+=1

  filesize = os.stat(f"./imgs/{image_name}").st_size
  im = Image("",filesize,image_name,"",regions)

  if count<train:
    image_sample_of = 'via_region_data_train'
    shutil.copy(f"imgs/{image_name}", f"sb_sign/train/{image_name}")
  else:
    image_sample_of = 'via_region_data_val'
    shutil.copy(f"imgs/{image_name}", f"sb_sign/val/{image_name}")

  if not outputs[image_sample_of]:
    outputs[image_sample_of] = {
      f"{im.filename}{im.size}":{
        "fileref":im.fileref,
        "size":im.size,
        "filename":im.filename,
        "base64_img_data":im.base64_img_data,
        "file_attributes": {},
        "regions": regions
      }
    }
  else:
    newImage = {
      f"{im.filename}{im.size}":{
        "fileref":im.fileref,
        "size":im.size,
        "filename":im.filename,
        "base64_img_data":im.base64_img_data,
        "file_attributes": {},
        "regions": regions
      }
    }
    outputs[image_sample_of] = dict(outputs[image_sample_of], **newImage)
    



f = open(f"./sb_sign/train/via_region_data.json", 'w')
f.write(json.dumps(outputs['via_region_data_train']))
f.close()


f = open(f"./sb_sign/val/via_region_data.json", 'w')
f.write(json.dumps(outputs['via_region_data_val']))
f.close()
