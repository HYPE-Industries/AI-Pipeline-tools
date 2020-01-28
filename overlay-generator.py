# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020

import argparse;
import json;
import os;
import shutil;
import sys;
from PIL import Image, ImageDraw;
from colored import fg, bg, attr;

# Options
parser = argparse.ArgumentParser(description='Merge HYPE Annotation Format Folder. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)');
parser.add_argument( "-i", "--input", help="Input directory. Contains /annotations and /images directories as dictated by HYPE Annotation format. Multiple directories separated by space. (required)" );
parser.add_argument( "-o", "--output", help="Output directory to create. Directory must not exist. (required)" );
parser.add_argument( "-n", "--name", default="awd", help="Dataset prefix name. Prepended to all files exported." );


# Setup all the arguments
args = parser.parse_args();
output_dir   = args.output;
input_dir    = args.input; # image directory
dataset_name = args.name; # dataset name
est_img      = 0;  # Est num of total images
image_cnt    = 0;  # Total num of images transferred

# Progress Bar # Vladimir Ignatyev <ya.na.pochte@gmail.com>
def progress(count, total, status=''):
    bar_len = 60;
    filled_len = int( round( bar_len * count / float( total ) ) );
    percents = round( 100.0 * count / float( total ), 1);
    bar = '=' * filled_len + '-' * ( bar_len - filled_len );
    sys.stdout.write('[%s] %s%s ...%s\r' % ( bar, percents, '%', status ) );
    sys.stdout.flush();

print ( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );

# Create Directory
try:
    os.mkdir( output_dir );
except FileExistsError:
    print( "Error: Directory \'" + output_dir + "\' already exists" );
    exit();

# Validate all inputs
if os.path.isdir( os.path.join( os.getcwd(), input_dir ) ) and os.path.isdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ) and os.path.isdir( os.path.join( os.getcwd(), input_dir, "images" ) ):
    est_img += len( os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ) );
else:
    print( "Error: Failed to locate. The folders must contain a HYPE annotation format with a /images folder and /annotations folder." );
    exit();

# Start Image Loop
for manifest in os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ):
    with open( os.path.join( os.getcwd(), input_dir, "annotations", manifest ), "r" ) as _manifest:
        data = json.load( _manifest ) # read file
        img_file = os.path.join( os.getcwd(), input_dir, "images", data[ "file" ] ); # image file
        img = Image.open( img_file ); # open file

        draw = ImageDraw.Draw( img );

        for label in data[ "annotation" ]:
            draw.rectangle( [ label[ "bndbox" ][ "xmin" ], label[ "bndbox" ][ "ymin" ], label[ "bndbox" ][ "xmax" ], label[ "bndbox" ][ "ymax" ] ], outline="blue" );
            draw.rectangle( [ label[ "bndbox" ][ "xmin" ], label[ "bndbox" ][ "ymax" ], label[ "bndbox" ][ "xmax" ], label[ "bndbox" ][ "ymax" ] + 20 ], outline="blue", fill="blue" );
            draw.text( [ label[ "bndbox" ][ "xmin" ] + 5, label[ "bndbox" ][ "ymax" ] + 5 ], label[ "label" ] );

        img.save( os.path.join( os.getcwd(), output_dir, dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".jpg" ), "JPEG", quality=100 ); # save images to output
        image_cnt = image_cnt + 1; # transfer image count
        img.close(); # close image
        progress( image_cnt, est_img, "Overmapping" );

print( "\n " + str( image_cnt ) + " images overlayed (" + input_dir + ") to (" + output_dir + ")" );
