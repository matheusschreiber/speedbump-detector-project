import json
import os
import shutil

def load_annotation(image_key):
  with open(os.path.join('annotations', '{:s}.json'.format(image_key)), 'r') as fid:
    anno = json.load(fid)
  return anno

def load_val_samples():
  with open(os.path.join('splits','train.txt'), 'r') as file:
    validation = file.read()
  return validation.split('\n')

def filter_road_bump():
  validation_samples = load_val_samples()
  count=0
  if os.path.isdir('bumps'): shutil.rmtree('bumps')
  os.makedirs('bumps')
  for sample in validation_samples:
    source_path = os.path.join('images', sample + '.jpg')
    destination_path = os.path.join('bumps', sample + '.jpg')

    if not os.path.exists(source_path): continue

    annotation = load_annotation(sample)

    for sign in annotation['objects']:
      if 'bump' in sign['label']:
        count+=1
        shutil.copy(source_path, destination_path)
        print(f"Copied {source_path} to {destination_path}")
    
  print(f"{count} signs")

def generate_zip():
  output_path = os.path.join('output')
  if os.path.isdir(output_path):
    shutil.rmtree(output_path)
  os.makedirs(output_path)

  images_path = os.path.join(output_path, 'imgs')
  shutil.copytree('bumps', images_path)
  
  with open(os.path.join(output_path, 'speedbumps.csv'), 'x') as output_csv:
    validation_samples = load_val_samples()

    # FIXME: problema para tirar placas muito diferentes da pasta bumps
    # pois tem que tirar as anotations do speedbumps.csv também
    for sample in validation_samples:
      if not os.path.exists(os.path.join('annotations', '{:s}.json'.format(sample))): continue

      annotation = load_annotation(sample)

      for sign in annotation['objects']:
        if not 'bump' in sign['label']: continue

        xmin = sign['bbox']['xmin']
        xmax = sign['bbox']['xmax']
        ymin = sign['bbox']['ymin']
        ymax = sign['bbox']['ymax']

        
        xmin_relative = xmin/annotation['width']
        xmax_relative = xmax/annotation['width']
        ymin_relative = ymin/annotation['height']
        ymax_relative = ymax/annotation['height']

        output_csv.write(f"VALIDATION,imgs/{sample}.jpg,SpeedBumpSign,{xmin_relative:.4f},{ymin_relative:.4f},,,{xmax_relative:.4f},{ymax_relative:.4f},,\n")
    
    shutil.make_archive('dataset', 'zip', output_path) 



if __name__ == '__main__':
  # filter_road_bump()
  generate_zip()
