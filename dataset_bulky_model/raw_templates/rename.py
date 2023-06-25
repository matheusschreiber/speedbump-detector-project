import os
import shutil

count = 19
os.makedirs('new_provisory')

for item in os.listdir('provisory'):
	
	shutil.copy(f'provisory/{item}', f'new_provisory/{count:04d}.png')

	count+=1
