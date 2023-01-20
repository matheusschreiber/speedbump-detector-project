# Dataset cleaning

## Preparation

The scale follows:

- Images bigger than 640 pixels on both dimensions: scale it down to 640 on lower dimension
- Images smaller than 640 pixels on one dimension: 
  - if picture is higher tan 200x200 than scale it up to 640 on lower dimension
  - discart it otherwise

## Script

The following script rename all the files to follow an index order, and then copy to the templates folder to be used on dataset generation

```bash
cd raw_templates/ppm

index=0

for i in $( ls ); do
  mv $i $(printf "%04d.ppm" $index)
  cp $(printf "%04d.ppm" $index) ../../templates
  ((index=index+1))
done
```