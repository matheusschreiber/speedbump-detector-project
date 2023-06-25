# Bulky dataset

## Proposal

This dataset is designed to train the bulky model on tensorflow standard procedure (not the lite version). Doing so, we are able to compare the performance of a big trained model and a small, compact model, and weight the differences.

## Description

The images have the following configurations:

- 58.000 images
- min width of 1500 pixels
- min height of 1500 pixels
- various contexts (COCO), such as:

<table>
  <tr>
    <td>'dog'</td>
    <td>'cat'</td>
    <td>'person'</td>
    <td>'bird'</td>
    <td>'dining table'</td>
    <td>'banana'</td>
  </tr>
  <tr>
    <td>'apple'</td>
    <td>'pizza'</td>
    <td>'donut'</td>
    <td>'sandwich'</td>
    <td>'carrot'</td>
    <td>'orange'</td>
  </tr>
  <tr>
    <td>'chair'</td>
    <td>'cake'</td>
    <td>'toilet'</td>
    <td>'bed'</td>
    <td>'couch'</td>
    <td>'hot dog'</td>
  </tr>
</table>

## Sample Generation

The sample generation is based on the same algorithm as the other datasets on this repository, but now the annotations are in the PASCAL VOC format.





