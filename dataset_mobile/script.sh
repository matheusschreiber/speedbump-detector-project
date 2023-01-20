#!/bin/bash

#This script is to rename all files on ppm folder to indexes

cd raw_templates/ppm

index=0

for i in $( ls ); do
  mv $i $(printf "%04d.ppm" $index)
  cp $(printf "%04d.ppm" $index) ../../templates
  ((index=index+1))
done