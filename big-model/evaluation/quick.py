import os

count = 0
for item in os.listdir('images'):

  if ' 1.jpg' in item:
    os.rename(os.path.join('images', item), os.path.join('images', item.replace(' 1.jpg', '.jpg')))
    os.rename(os.path.join('test_labels',item.replace('.jpg', '.xml')), os.path.join('test_labels', item.replace(' 1.jpg', '.xml')))
    count+=1

  if ' 2.jpg' in item:
    os.rename(os.path.join('images', item), os.path.join('images', item.replace(' 2.jpg', '.jpg')))
    os.rename(os.path.join('test_labels',item.replace('.jpg', '.xml')), os.path.join('test_labels', item.replace(' 2.jpg', '.xml')))
    count+=1

print(f"{count}/{len(os.listdir('images'))}")