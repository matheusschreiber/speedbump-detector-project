# Annotations

The `main.py` file takes care of the creation of new annotated dataset for testing the model. It uses labels made with [LabelImg](https://pypi.org/project/labelImg/1.4.0/), and their respective images.

As described in LabelImg's documentation, the label generated is a `.txt` file with the coordinates of 2 points of a rectangle. So the script translates these coordinates to the `Tensorflow Lite` sample configuration.

> The annotation type used in `LabelImg` is `YOLO.`

Once the annotations are already generated and in the same directory as their respective images, then execute the script to generate the `output` folder with the `images` and the `.csv` file.

To run the script you have to pass the input and output paths as described below:

```bash

# 'annotations' directory includes all images and all annotations
# 'output' directory is generated from scratch if it doesn't exists

python3 main.py --in-path annotations --out-path output
```

As the results, the `output` folder will contain the following `.csv`

```csv
TEST,imgs/IMG_20230318_162749826.jpg,SpeedBumpSign,0.5957,0.4162,,,0.0794,0.0966,,
TEST,imgs/IMG_20230318_171235798.jpg,SpeedBumpSign,0.4261,0.3560,,,0.1283,0.1027,,
TEST,imgs/IMG_20230318_171733444.jpg,SpeedBumpSign,0.4953,0.4772,,,0.0908,0.0760,,
TEST,imgs/IMG_20230318_171004959_HDR.jpg,SpeedBumpSign,0.4889,0.4920,,,0.0449,0.0463,,

...
```
