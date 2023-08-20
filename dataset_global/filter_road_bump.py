import json
import os
import shutil

def generate_zip(output_path):
  shutil.make_archive('dataset', 'zip', output_path) 

def load_annotation(image_key):
  try:
    with open(os.path.join('annotations', '{:s}.json'.format(image_key)), 'r') as fid:
      anno = json.load(fid)
    return anno
  except:
    return None

def load_val_samples():
  with open(os.path.join('splits','train.txt'), 'r') as file:
    validation = file.read()
  return validation.split('\n')

def load_all_samples():
  all = []
  
  with open(os.path.join('splits','val.txt'), 'r') as file:
    val = file.read()
  all =  all + val.split('\n')

  with open(os.path.join('splits','test.txt'), 'r') as file:
    test = file.read()
  all =  all + test.split('\n')

  with open(os.path.join('splits','train.txt'), 'r') as file:
    train = file.read()
  all =  all + train.split('\n')

  return all

def filter_road_bump():
  samples = load_all_samples()
  count=0
  if os.path.isdir('bumps'): shutil.rmtree('bumps')
  os.makedirs('bumps')
  for sample in samples:
    source_path = os.path.join('images', sample + '.jpg')
    destination_path = os.path.join('bumps', sample + '.jpg')

    if not os.path.exists(source_path): continue

    annotation = load_annotation(sample)
    if not annotation:
      print(f'Problema com {sample}')
      continue

    for sign in annotation['objects']:
      if 'bump' in sign['label']:
        count+=1
        shutil.copy(source_path, destination_path)
        print(f"Copied {source_path} to {destination_path}")
        #shutil.move(source_path, destination_path)
        #print(f"Moved {source_path} to {destination_path}")
    
  print(f"{count} signs")

def create_csv():
  output_path = os.path.join('output')
  if os.path.isdir(output_path):
    shutil.rmtree(output_path)
  os.makedirs(output_path)

  # images_path = os.path.join(output_path, 'bumps')
  # shutil.copytree('bumps', images_path)
  
  with open(os.path.join(output_path, 'speedbumps.csv'), 'x') as output_csv:
    samples = load_all_samples()

    # FIXME: problema para tirar placas muito diferentes da pasta bumps
    # pois tem que tirar as anotations do speedbumps.csv também
    for sample in samples:
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
    
    # generate_zip(output_path)




if __name__ == '__main__':
  filter_road_bump()
  create_csv()



