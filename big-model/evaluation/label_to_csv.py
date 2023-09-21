"""
  This scripts converts the csv file with this:
    filename,width,height,class,xmin,ymin,xmax,ymax
    IMG_20230318_165704697.jpg,1350,1792,SpeedBumpSign,623,463,812,676
  
  To the speedbuumps.csv format like this:
    TRAINING,imgs/IMG_20230318_165704697.jpg,SpeedBumpSign,0.3913,0.2360,,,0.4213,0.2720,,
"""

output = []

with open('test_labels.csv', 'r') as f:
  for line in f:
    data = line.split(',')
    if data[0] == 'filename': continue

    xmin = int(data[4])/int(data[1])
    ymin = int(data[5])/int(data[2])
    xmax = int(data[6])/int(data[1])
    ymax = int(data[7])/int(data[2])
    print(data[0])
    output.append(f"TRAINING,imgs/{data[0]},SpeedBumpSign,{xmin:.4f},{ymin:.4f},,,{xmax:.4f},{ymax:.4f},,")

output_str = '\n'.join(output)

with open('speedbumps.csv', 'w') as f:
  f.write(output_str)

  
  
