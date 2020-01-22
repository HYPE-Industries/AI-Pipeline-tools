# HYPE Industries AI Pipeline Tools
bla bla

<hr>

## Dataturk's Downloader
Use a `JSON` file provided by Dataturk. These json file have the annotations for each photograph and have a url to the image. This python script will download it from the url and convert the annotations to the HYPE annotations format. You should be in the main directory of the HYPE AI Tools.

<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input JSON file. Path to dataturk dataset file. | required |
|`--output` | `-o` | Output directory to create. Directory must not exist.<br>In HYPE Annotations format. | required |
|`--name`|`-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |
|`--dataset` | `-d` |Dataset name. Full name of dataset for information. | defualt `untitled` |


<b>Usage</b>
```python
# CLI
py "dataturk-download.py" --input <json file> --output <export folder>

# Example
py "dataturk-download.py" --input "AIDA datasets.json"  --output "output_folder" --name "prism" --dataset "Prism Dataset July"
py "dataturk-download.py" --input "AIDA datasets.json"  --output "output_folder"
```

<hr>

## Dataset Merge
The dataset merge tool can be used to combined multiple HYPE annotated datasets. These data sets MUST be in the HYPE annotated format. The tool additionally can crosscheck images that are being merged to make sure there aren't duplicates.

<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input directory. Contains `/annotations` and `/img` directories<br> as dictated by HYPE Annotation format. Multiple directories<br>separated by space. | at least 1 |
|`--output` | `-o` | Output directory to create. Directory must not exist. | required |
| `--name` | `-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |
| `--crosscheck` | `-c` | Removes image if duplicated. Num is hash amount off. <br> Set to `-1` to disable. | default `10`|

<b>Usage</b>
```python
# CLI
py "merge.py" --output <output folder> --input <input folder 1> <input folder 2> --crosscheck -1

# Example
py "merge.py" --output "hello_world" --input "bro1" "bro2" --crosscheck 100
py "merge.py" --output "hello_world" --input "bro1" "bro2"
```

<hr>


## Manipulator
The manipulator tool creates duplicates of images. It applies filters, rotates, and pixelates the image in all combinations. It will also alter the cords.

<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input directory. Contains `/annotations` and `/img` directories<br> as dictated by HYPE Annotation format. | required |
|`--output` | `-o` | Output directory to create. Directory must not exist. | required |
| `--name` | `-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |
| `--dictate` | `-d` | Adds notes to annotation file of what process done to pic. | optional |

<b>Usage</b>
```python
# CLI
py manipulator.py --input <path to directory> --output <path to output>

# Example
py manipulator.py --input <path to directory> --output <path to output> --name "prism"
py manipulator.py --input <path to directory> --output <path to output> --dictate
```

<hr>

## Plot Point Preview
Use the point plot preview to verify that your point of an annotated image are correct. You can open any image that is in the HYPE Annotation Format.

<b>Cord Location</b>

| Position | Color | X | Y |
|---|---|---|---|
| top left | BLUE | xmin | ymin |
| top right | RED | xmax | ymin |
| bottom right | GREEN | xmax | ymax |
| bottom left | ORGANGE | xmin | ymax |


<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input JSON file. Path to HYPE Annotation file. | required |
| `--point` | `-p` | Adds point location in corners | optional |

<b>Usage</b>
```python
# CLI
py plot-point-preview.py --input <path to json annotation>

# Example
py plot-point-preview.py --input "/output3/annotations/awd_1.json" --point # enable points
py plot-point-preview.py --input "/output3/annotations/awd_1.json"         # no points
```

<hr>

## Darkflow Converter
Use the Darkflow converter to convert from HYPE Annotation format. It will produce an `/img` folder with all the `.jpg` images and an `/annotations` folder with the `.xml` formatted data. The images and xml's correspond to each other by name.

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input directory. Contains `/annotations` and `/img` directories<br> as dictated by HYPE Annotation format. | required |
|`--output` | `-o` | Output directory to create. Directory must not exist. | required |
| `--name` | `-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |

<b>Usage</b>
```python
# CLI
py to-darkflow.py --input <path to directory> --output <path to output> --name <file prefix>

# Example
py to-darkflow.py --input "output" --output "output_new" --name "prism"
py to-darkflow.py --input "output" --output "output_new"
```

<hr>

## HYPE Annotations Format
There is a folder with an folder label `/img` and `/annotations`. The `/img` directory stores `.jpg` photographs with the same name corresponding to a `.json` file storing the annotation data in the `/annotations` folder.

<b>Point Plotting</b><br>
The top left of the image is the origin (0,0). These number therefor represent the x and y distance in pixels from the origin.

| x  | y  | position  |
|---|---|---|
| xmin | ymin | top left     |
| xmax | ymin | top right    |
| xmax | ymax | bottom right |
| xmin | ymax | bottom left  |

<b>Directory Structure</b>
- /output_folder
  - /img
    - awd_1.jpg
    - awd_2.jpg
  - /annotations
    - awd_1.json
    - awd_2.json

<b>Format</b>
```json
{
  "dataset": "Name of set",
  "publisher": "Company Name",
  "file": "photograph name in /img folder",
  "date": "date this file is created",
  "annotation": [
    {
      "label": "class",
      "bndbox": {
        "xmin": "xmin",
        "ymin": "ymin",
        "xmax": "xmax",
        "ymax": "ymax"
      }
    }
  ],
  "size": {
    "width": "width of image",
    "height": "height of image"
  }
}
```

<b>Example</b> (/annotations/awd_1.json)
```json
{
  "dataset": "Active Weapon Detection July",
  "publisher": "HYPE Industries 2020",
  "file": "awd_1.jpg",
  "date": "2020-01-21 09:43:47.550646",
  "annotation": [
    {
      "label": "active_weapon_class_2",
      "bndbox": {
        "xmin": 733.0,
        "ymin": 142.0,
        "xmax": 920.0,
        "ymax": 382.0
      }
    }
  ],
  "size": {
    "width": 1006,
    "height": 563
  }
}
```
