# HYPE Industries AI Pipeline Tools
The HYPE Industries AI Pipeline are to designed to assist in the process of dealing with large machine vision datasets. Everything is imported and converted to the HYPE Annotation Format (HAF). Then the data can be merged, manipulated, and masked. After all your changes are made, you can use the exporter to convert it to the format you need it in. The HYPE Annotation Format is the best way to store your datasets in, as many different types of data can be converted into one standard format. In additional to all this there is also a build in Bing Image scrapper, to help you collect data for manual annotation, that can crosscheck all your datasets to ensure there is no duplicated images.

<hr>

## Import to HAF
The import script, will help you import datasets from other sources into HAF. Some of the supported formats are datasets from Dataturk or LabelBox. This means you can use a JSON file provided by these services and the HAF Importer will download and convert the files.


<br>


<b>Options</b><br>
The options for the CLI command are as followed. The DS information (ex. `ds_number` and `ds_source`), is information for "long term" storage of the dataset, and this information will be placed in the manifest file.

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Location of the file or directory, containing the dataset information. | required |
|`--output` | `-o` | Output directory name, to create, with HYPE Annotations. | required |
|`--format`|`-f` | Format to convert from. See documentation for list of acceptable formats. | required |
|`--ds_number`| N/A | Dataset number ex. DS1, DS2, DS3 | required |
|`--ds_source`| N/A | Dataset Source ex. Web Source, Sythetic Data, Web Video, Live Capture, 3D Model | required |
|`--ds_date`| N/A | Date the dataset was generated ex. JAN2020, DEC2019 | required |
|`--ds_notes`| N/A | Additional notes to include. | optional |


<br>
<br>


<b>Formats</b><br>
These are the acceptable formats that can be imported. To select one of these inputs use `--format` or `-f`, followed by the Format Code.

| Name | Format Code | Source Type | Description |
|----| ----- |----|--- |
| Dataturk | `dataturk` | Dataturk json file | Bounding box annotation only |
| LabelBox | `labelbox` | LabelBox json file | Bounding box annotation only |
| Edge Case | `edgecase` | Edge Case Directory | Bounding box annotation only |


<br>
<br>


<b>Usage Examples</b>
```shell
# CLI Example
py "import.py" --input AIDA-datasets.json  --output output_folder --format labelbox --ds_number DS5 --ds_source "Web Source" --ds_date JAN2020
```


<hr>

## Export
This will export you HYPE Annoation format to another format option. It can export to only darkflow currently but support for darknet is coming soon. When exporting depending on the format a class list will come in the directory, along with a HYPE Annotation Format Manifest.


<br>


<b>Options</b><br>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Location of the file or directory, containing the dataset information. | required |
|`--output` | `-o` | Output directory name, to create, with HYPE Annotations. | required |
|`--format`|`-f` | Format to convert to. See documentation for list of acceptable formats. | required |


<br>
<br>


<b>Formats</b><br>
These are the acceptable formats that can be imported. To select one of these inputs use `--format` or `-f`, followed by the Format Code.

| Name | Format Code | Source Type | Description |
|----| ----- |----|--- |
| Darkflow | `darkflow` | generators directory for darkflow | Bounding box annotation only |
| Darknet | `darknet` | generators directory for darknet | Bounding box annotation only |


<br>
<br>


<b>Usage Examples</b>
```shell
# CLI Example
py "export.py" --input input_folder --output output_folder --format darkflow
```


<hr>

## Mask Generator
Comming soon

<hr>

## Merge datasets
After all your datasets have been created you can merge them together for exporting. Don't use the merge system to merge a already merged file. If you need to merge more in, you must merge all the HAF again. This can be used to merge multiple datasets together. This will create a custom manifest with all the sub dataset information stored in the manifest.

<b>Options</b><br>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Location of HAF directory, containing the dataset information. Put space inbetween to add multiple locations. | required |
|`--output` | `-o` | Output directory name, to create, with HYPE Annotations. | required |
|`--name`| `-n` | Dataset prefix name. Prepended to all files exported. | `pwd` |



<hr>

## Annotation Preview
With the help of the Annoation Preview you can select an annotation file (HAF) and preview the bounding box in a preview window. This tool can be very helpful when designing import tools to ensure that you have imported in to HAF correctly.


<br>


<b>Cord Location</b><br>
These colors signify each corner of the bounding box. This helps you ensure the bounding box is in the correct position as well in the right orientation.

| Position | Color | X | Y |
|---|---|---|---|
| top left | BLUE | xmin | ymin |
| top right | RED | xmax | ymin |
| bottom right | GREEN | xmax | ymax |
| bottom left | ORGANGE | xmin | ymax |


<br>


<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input JSON file. Path to HYPE Annotation file. | required |
| `--point` | `-p` | Adds point location in corners | optional |


<br>


<b>Usage</b>
```shell
# CLI
py preview.py --input <path to json annotation>

# Example
py preview.py --input "/output3/annotations/awd_1.json" --point # enable points
py preview.py --input "/output3/annotations/awd_1.json"         # no points
```


<hr>

## Bing Image Scrapper
Using the bing image downloader you can scrap a large amount of images from bing. Additionally, it will crosscheck all directories in the main folder both just directories of images, and HYPE Annotation folders. You can set custom crosscheck folder using the `--crosscheck` option.

It will ask you to check the temp directory, during this time go to this directory and make sure all the images are valid, then press enter. After the process is done delete all the images left in the temp folder.

This requires the `modules/chromedriver.exe` to run, if you are downloading more than 100 images.

<br>

<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--output` | `-o` | Output directory name, with downloaded images. | required |
|`--url` | `-i` | Bing Image URL will be scrapped for images. | required |
|`--crosscheck` | `-c` | By defualt will search all first level directories in the root folder, including `/images` for HYPE Annotations. Pass list of directories with space in-between, to define custom directories to crosscheck. Use `-1` to disable crosscheck. | default all dir in `~/` |
|`--num_images`|`-n` | Number of images to download to directory. | default `100` |

<br>

<b>Usage</b>
```shell
# url download
py "image-scrapper.py" --output "output folder" --url "url" -n 100

# keyword download
py "image-scrapper.py" --output "output folder" --url "www.bing.com/search?q=dogs" -n 1000
```



<hr>

## HYPE Annotation Format
The HYPE Annotation Format (HAF) was built to simplify data collection for machine vison. Consisting of a photograph and a matching annotation file, converting all your datasets into HAF, processing them, and then converting them out can save time on your Machine Vision Pipeline. It is import to note that HAF1 only supports bounding box type labeling.

<br>

<b>Point Plotting</b><br>
The top left of the image is the origin (0,0). These number therefor represent the x and y distance in pixels from the origin.

| x  | y  | position  |
|---|---|---|
| xmin | ymin | top left     |
| xmax | ymin | top right    |
| xmax | ymax | bottom right |
| xmin | ymax | bottom left  |

<br>

<b>Directory Structure</b><br>
The following is the directory Structure that HAF1 is placed in. This consistant format play a vital role in how HAF is able to easily move and manipulate large datasets.
```
output_folder
  └ manifest.json
  └ images
    └ DS1_001.jpg
    └ DS1_002.jpg
    └ DS1_003.jpg
    └ ...
  └ annotations
    └ DS1_001.json
    └ DS1_002.json
    └ DS1_003.json
    └ ...
```

<br>

<b>Dataset Manifest</b><br>
The dataset manifest is located in every dataset directory, and stores important information about the dataset. For example the manifest stores class, total image count, source of annotations, and dataset name, When datasets are merged this information will go with it.

```JSON
{
  "format": "HYPE Annotation Format v1.0.0",
  "name": "DS1 JAN2020 - Web Source (HAF)",
  "number": "DS1",
  "source": "Web Source",
  "date": "JAN2020",
  "total": 12,
  "birth": "2020-01-31 14:50:10.689196",
  "class": [
    "active_weapon_class_2"
  ],
  "note": "Import note on dataset"
}
```

<br>

<b>Annotation Format</b><br>
```json
{
  "dataset": {
    "name": "DS1 JAN2020 - Web Source (HAF)",
    "number": "DS1",
    "source": "Web Source"
  },
  "file": "DS1_00.jpg",
  "date": "2020-01-31 14:49:51.617040",
  "annotation": [
    {
      "label": "active_weapon_class_2",
      "bndbox": {
        "xmin": 296.4862393649428,
        "ymin": 478.850186869146,
        "xmax": 476.2456128381758,
        "ymax": 630.6807339252167
      }
    }
  ],
  "size": {
    "width": 1211,
    "height": 681
  }
}
```

<hr>

## Research
This section details some of the "research" that has been done when building this project.

<b>Manipulated Images</b><br>
There was originally the plan to take all images collected in a dataset and manipulate them in different ways. Filters would be applied to them, and they would be rotated and mirrored. This process would be done to every images, resulting in hundreds of sub-images for each images. This process was performed, and it did not go well at all. The system had a hard time recognizes images, and even had ghost recognition when images were manipulated. After these results that functionality was removed and would not be recommended for any project.

<b>synthetic data</b>
We have been using video games to generate data for weapon detection software, and are happy to report drastic improvements in speed, accuracy and reliability in our CNN for Prism.

<hr>


## FIXME
- test image scrapper
- add converter for edgecase
- rebuild overlay generator (BACKLOG)


<br>


## Changelog
<b>February 19, 2020</b>
- export documentation
- updated system to use bing instead of google
- updates to `.gitignore`, now place working models in the workspace dir

<b>February 18, 2020</b>
- merger now supports manifest system
- merger now uses progress bar implemtation
- exporter updated

<b>February 2, 2020</b>
- Google Image Scrapper Updated

<b>February 1, 2020</b>
- Update preview tool, now applies label to bounding box

<b>January 31, 2020</b>
- Conversions to HYPE Annotation format will now be done from `import.py`.
- dataturk downloader removed, and now ran from `import.py`.
- importer now supports labelbox
- modules folder, has module for progress bar
- importer now exports a manifest file, with critical information for the dataset.
- removed manipulator

<b>January 28, 2020</b>
- Updated all jpeg exports to be at 100%
- Google Image Scrapper Completed, with built in merge
- export folder for images is now `/images`

<b>January 23, 2020</b>
- Error when naming the attribute in the xml, the name ended in `.xml` and it should of ended in `.jpg`.

<b>January 22, 2020</b>
- Error in naming scheme when generating the xml, cause the file name attribute not to have floating zeros that matched the file name.
- Convert to Darkflow from HYPE annotated format using the `to-darkflow.py`.
- Generate bounding box preview of all images in a package, using `overlay-generator.py`.
- Manipulator updated to support new HYPE annotated format.
- Added argparse to all scripts allowing options .
- See live progress bar as image processing progresses.

<b>January 21, 2020</b>
- Plot Point Preview allows you to preview a bounding box, by opening an XML file.
- Merge Script allows you to combined multiple HYPE annotated packages together.
- Dataturk downloader, can now download images from online, using the dataturk json format.



































<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>



# Old Documents - to be fixed
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
```shell
# CLI
py "dataturk-download.py" --input <json file> --output <export folder>

# Example
py "dataturk-download.py" --input "AIDA datasets.json"  --output "output_folder" --name "prism" --dataset "Prism Dataset July"
py "dataturk-download.py" --input "AIDA datasets.json"  --output "output_folder"
```

<hr>

## Google Downloader
Using the google image downloader you can scrap a large amount of images from google. Additionally, it will crosscheck all directories in the main folder both just directories of images, and HYPE Annotation folders. You can set custom crosscheck folder using the `--crosscheck` option.

It will ask you to check the temp directory, during this time go to this directory and make sure all the images are valid, then press enter. After the process is done delete all the images left in the temp folder.

<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--url` | `-i` | Google Search url or Image Path for `--similar_img` | optional |
|`--similar_images` | `-s` | Will download related images. Only for use with direct image url. | optional |
|`--keywords` | `-k` | List of keywords separated by a space. | optional. |
|`--related_images` | `-r` | Will download related images. Only for use with keywords | optional |
|`--crosscheck` | `-c` | By defualt will search all first level directories in the root folder, including `/images` for HYPE Annotations. Pass list of directories with space in-between, to define custom directories to crosscheck. | default all dir in `~/` |
|`--num_images`|`-n` | Number of images to export. For each keyword. | default `100` |

<b>Usage</b>
```shell
# url download
py "google-image-scrapper.py" --output "output folder" --url "url" -n 100

# keyword download
py "google-image-scrapper.py" --output "output folder" --keywords "dog" "cat" -n 100
```


<hr>

## Dataset Merge
The dataset merge tool can be used to combined multiple HYPE annotated datasets. These data sets MUST be in the HYPE annotated format. The tool additionally can crosscheck images that are being merged to make sure there aren't duplicates.

<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input directory. Contains `/annotations` and `/images` directories<br> as dictated by HYPE Annotation format. Multiple directories<br>separated by space. | at least 1 |
|`--output` | `-o` | Output directory to create. Directory must not exist. | required |
| `--name` | `-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |
| `--crosscheck` | `-c` | Removes image if duplicated. Num is hash amount off. <br> Set to `-1` to disable. | default `10`|

<b>Usage</b>
```shell
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
|`--input` | `-i` | Input directory. Contains `/annotations` and `/images` directories<br> as dictated by HYPE Annotation format. | required |
|`--output` | `-o` | Output directory to create. Directory must not exist. | required |
| `--name` | `-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |
| `--dictate` | `-d` | Adds notes to annotation file of what process done to pic. | optional |

<b>Usage</b>
```shell
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
```shell
# CLI
py plot-point-preview.py --input <path to json annotation>

# Example
py plot-point-preview.py --input "/output3/annotations/awd_1.json" --point # enable points
py plot-point-preview.py --input "/output3/annotations/awd_1.json"         # no points
```

<hr>

## Overlay Generator
Generate an overlay of the bounding box over each image. Outputs only the images to a directory. Must use a input directory that is an HYPE Annotate format.

<b>Options</b>

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input directory. Contains `/annotations` and `/images` directories<br> as dictated by HYPE Annotation format. | required |
|`--output` | `-o` | Output directory to create. Directory must not exist.<br>Only outpute the pictures. | required |
| `--name` | `-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |

<b>Usage</b>
```shell
# CLI
py overlay-generator.py --input <path to json annotation> --output <path to output>

# Example
py overlay-generator.py --input "output3" --output "output4" # enable points
```


<hr>

## Darkflow Converter
Use the Darkflow converter to convert from HYPE Annotation format. It will produce an `/images` folder with all the `.jpg` images and an `/annotations` folder with the `.xml` formatted data. The images and xml's correspond to each other by name.

| Name | Alias | Description | required |
|---   | ----- | ---- | --- |
|`--input` | `-i` | Input directory. Contains `/annotations` and `/images` directories<br> as dictated by HYPE Annotation format. | required |
|`--output` | `-o` | Output directory to create. Directory must not exist. | required |
| `--name` | `-n` | Dataset prefix name. Prepended to all files exported. | default `awd` |

<b>Usage</b>
```shell
# CLI
py to-darkflow.py --input <path to directory> --output <path to output> --name <file prefix>

# Example
py to-darkflow.py --input "output" --output "output_new" --name "prism"
py to-darkflow.py --input "output" --output "output_new"
```

<hr>

## HYPE Annotations Format
There is a folder with an folder label `/images` and `/annotations`. The `/images` directory stores `.jpg` photographs with the same name corresponding to a `.json` file storing the annotation data in the `/annotations` folder.

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
  - /images
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
  "file": "photograph name in /images folder",
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

<hr>
