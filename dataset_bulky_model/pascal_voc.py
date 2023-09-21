import cv2
import os
import shutil
from pascal_voc_writer import Writer
from tqdm import tqdm
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

SPEED_BUMP_THRESHOLD=15

def pascal_voc(out_path, img_out_path, bboxes, nb_imgs_generated):
  annotations_path = os.path.join(out_path, "annotations_pascal_voc")
  if not os.path.isdir(annotations_path): os.makedirs(annotations_path)

  image = cv2.imread(img_out_path)
  img_name = img_out_path.split('/')[-1]
  writer = Writer(f"{nb_imgs_generated:05d}_{img_name}", image.shape[1], image.shape[0])

  for bbox in bboxes:
    if int(bbox['category'])>=SPEED_BUMP_THRESHOLD: continue
    writer.addObject("SpeedBumpSign", bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax'])

  img_name = os.path.splitext(img_name)[0]
  anno_output_path = os.path.join(annotations_path, f"{img_name}.xml")
  writer.save(anno_output_path)

  # here enters some manipulation to fit the xml to the model needs
  old_tree = ET.parse(anno_output_path)
  old_root = old_tree.getroot()
  filename_element = old_root.find('filename')
  size_element = old_root.find('size')
  segmented_element = old_root.find('segmented')
  new_root = ET.Element('annotation')
  new_folder = ET.SubElement(new_root, 'folder')
  new_folder.text = 'images'
  new_filename = ET.SubElement(new_root, 'filename')
  new_filename.text = filename_element.text
  new_size = ET.SubElement(new_root, 'size')
  for dimension in size_element:
    dimension_element = ET.SubElement(new_size, dimension.tag)
    dimension_element.text = dimension.text
  new_segmented = ET.SubElement(new_root, 'segmented')
  new_segmented.text = segmented_element.text
  for object_element in old_root.findall('object'):
    name_element = object_element.find('name')
    pose_element = object_element.find('pose')
    truncated_element = object_element.find('truncated')
    difficult_element = object_element.find('difficult')
    bndbox_element = object_element.find('bndbox')
    new_object = ET.SubElement(new_root, 'object')
    new_name = ET.SubElement(new_object, 'name')
    new_name.text = name_element.text
    new_pose = ET.SubElement(new_object, 'pose')
    new_pose.text = pose_element.text
    new_truncated = ET.SubElement(new_object, 'truncated')
    new_truncated.text = truncated_element.text
    new_occluded = ET.SubElement(new_object, 'occluded')
    new_occluded.text = '0'
    new_difficult = ET.SubElement(new_object, 'difficult')
    new_difficult.text = difficult_element.text
    new_bnb = ET.SubElement(new_object, 'bndbox')
    for dimension in bndbox_element:
      new_dimension = ET.SubElement(new_bnb, dimension.tag)
      new_dimension.text = dimension.text

  ET.indent(new_root, '    ')
  xml_string = ET.tostring(new_root, encoding='utf-8')
  xml_pretty_string = minidom.parseString(xml_string).toprettyxml(indent="", newl='')
  xml_declaration = '<?xml version="1.0" ?>'
  xml_pretty_string = xml_pretty_string.replace(xml_declaration, "")
  with open(anno_output_path, 'w') as f:
    f.write(xml_pretty_string)

if __name__ == '__main__':

  # out_path = "output"
  # img_out_path = "output/imgs/00000_COCO_train2014_000000154725.jpg"
  # bboxes = [{'xmin': 516, 'ymin': 0, 'xmax': 557, 'ymax': 42, 'category': '0012'}, {'xmin': 648, 'ymin': 34, 'xmax': 681, 'ymax': 77, 'category': '0002'}]
  # pascal_voc(out_path, img_out_path, bboxes, 1)

  # out_path = 'output'
  # class_path = os.path.join(out_path, 'multiclass.csv')
  
  # with open(class_path) as f:
  #   reader_obj = csv.reader(f)
  #   previous_sample=""  
  #   bboxes=[]
  #   for row in tqdm(reader_obj):
  #     if row[0] != previous_sample:
  #       bboxes=[]
  #       previous_sample=row[0]

  #     img = cv2.imread(row[0])
  #     bbox = {
  #       'xmin': int(img.shape[1]*float(row[2])),
  #       'ymin': int(img.shape[0]*float(row[3])),
  #       'xmax': int(img.shape[1]*float(row[6])),
  #       'ymax': int(img.shape[0]*float(row[7])),
  #       'category': row[1]
  #     }
  #     bboxes.append(bbox)
      
  #     pascal_voc(out_path, row[0], bboxes)

  # for item in os.listdir('output/annotations_pascal_voc'):
  #   shutil.copy(f"output/annotations_pascal_voc/{item}", f"output/annotations/{item.split('.')[0]}.xml")
