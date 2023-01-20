# Speedbump Detector

This is a neural network envisioned to detect speedbumps signs, ~~with the potential to run it into a mobile environment later on~~ running on mobile devices. 🥳


## Dataset 

### Image backgrounds

The dataset is built merging templates and COCO (Common Objects in Context) images on these topics:

- 200 images on `dog`
- 200 images on `cat`
- 200 images on `person`
- 200 images on `bird`
- 200 images on `banana`
- 200 images on `sandwich`
- 200 images on `carrot`
- 200 images on `orange`
- 200 images on `apple`
- 200 images on `pizza`
- 200 images on `hot dog`
- 200 images on `donut`
- 200 images on `cake`
- 200 images on `chair`
- 200 images on `dining table`
- 200 images on `toilet`
- 200 images on `bed`
- 200 images on `couch`

> [Instructions on how to use the script on COCO](/script_coco/COCO_GETTING_STARTED.md)

### Templates

The template images where acquired via public access, and have the following properties:

- Dimensions: 70x70 pixels
- Color: yellow/orange
- Shape: rectangle/diamond

A total of 14 templates where used for this dataset creation

### Generating overlapped images for training

## Mobile Tensorflow Lite

> [Tensorflow Lite 2 colab](https://colab.research.google.com/drive/1D2elywD2a8bsWZPGSxYv3RZKiP_h1jLR#scrollTo=Gb7qyhNL1yWt) for GPU access to train the model

## First conditions

- Epochs: 50
- Batch size: 8
- AP: 0.7478128 (74%) 
- Average time: 2min

## Best conditions so far

- Epochs: __
- Batch size: __
- AP: __
- Average time: __


## Dataset layout

```
TRAINING,gs://cloud-ml-data/img/openimage/3/2520/3916261642_0a504acd60_o.jpg,Salad,0.0,0.0954,,,0.977,0.957,,
```
```
VALIDATION,gs://cloud-ml-data/img/openimage/3/2520/3916261642_0a504acd60_o.jpg,Seafood,0.0154,0.1538,,,1.0,0.802,,
```
```
TEST,gs://cloud-ml-data/img/openimage/3/2520/3916261642_0a504acd60_o.jpg,Tomato,0.0,0.655,,,0.231,0.839,,
```

## Speedbump dataset layout

```
TRAIN,imgs/00000_COCO_train2014_000000262260.jpg,SpeedBumpSign,0.4375,0.1007,,,0.5453,0.2623,,
```
```
TEST,imgs/00148_COCO_train2014_000000524366.jpg,SpeedBumpSign,0.6531,0.0000,,,0.7844,0.1944,,
```
```
VALIDATION,imgs/00149_COCO_train2014_000000114776.jpg,SpeedBumpSign,0.6813,0.3167,,,0.7516,0.4104,,
```