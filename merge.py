# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020

import argparse;
import json;
import os;
import datetime;
import imagehash;
import shutil;
import sys;
from modules import progress;
from PIL import Image, ImageMath;
from colored import fg, bg, attr;

# Options
parser = argparse.ArgumentParser(description='Merge HYPE Annotation Format Folder. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)');
parser.add_argument( "-i", "--input", nargs='*', help="Input directory. Contains /annotations and /images directories as dictated by HYPE Annotation format. Multiple directories separated by space. (required)" );
parser.add_argument( "-o", "--output", help="Output directory to create. Directory must not exist. (required)" );
parser.add_argument( "-n", "--name", default="pwd", help="Dataset prefix name. Prepended to all files exported." );

# Setup all the arguments
args = parser.parse_args();
output_dir    = args.output;
_input_dir    = args.input; # temp array of dirrectories
dataset_name  = args.name; # name of data set
input_dir     = []; # List of image dirrectories
img_hash      = []; # List of image hashes
manifest_list = []; # list of all manifest for merged datasets
est_img       = 0;  # Est num of total images
img_cnt       = 0;  # Total num of images transferred
img_scan      = 0;  # Total num of images attemeted to transferred


print ( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );


# Make sure Output and Input were set
if output_dir == None or input_dir == None:
    print( "Error: Output or Input Directory not set" );
    exit();


# Create Directory
try:
    os.mkdir( output_dir );
    os.mkdir( output_dir + "/images" );
    os.mkdir( output_dir + "/annotations" );
except FileExistsError:
    print( "Erro: Directory \'" + output_dir + "\' already exists" );
    exit();


# Validate all inputs
for dir in _input_dir:
    if os.path.isdir( os.path.join( os.getcwd(), dir ) ) and os.path.isdir( os.path.join( os.getcwd(), dir, "annotations" ) ) and os.path.isdir( os.path.join( os.getcwd(), dir, "images" ) ) and os.path.isfile( os.path.join( os.getcwd(), dir, "manifest.json" ) ):
        with open( os.path.join( os.getcwd(), dir, "manifest.json" ), "r" ) as _manifest:
            input_dir.append( os.path.join( os.getcwd(), dir ) );
            est_img += len( os.listdir( os.path.join( os.getcwd(), dir, "annotations" ) ) );
            manifest_list.append( json.load( _manifest ) );
    else:
        print( "Error: Failed to locate. The folders must contain a HYPE annotation format with a /images folder and /annotations folder and the manifest.json." );
        exit();


# Move to new directory
for dir in input_dir:
    for manifest in os.listdir( os.path.join( os.getcwd(), dir, "annotations" ) ):
        with open( os.path.join( os.getcwd(), dir, "annotations", manifest ), "r" ) as _manifest:
            data = json.load( _manifest ) # read file
            img_file = os.path.join( os.getcwd(), dir, "images", data[ "file" ] ); # image file

            if os.path.isfile( img_file ):
                img_scan = img_scan + 1; # add to scanned images
                img = Image.open( img_file ); # open file

                # Convert Image Modes
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new(img.mode[:-1], img.size, "#000" )
                    background.paste(img, img.split()[-1])
                    img = background;
                elif img.mode == 'P':
                    img = img.convert( "RGB" );


                img_hash.append( hash ); # add ti hash list
                img.save( os.path.join( os.getcwd(), output_dir, "images", dataset_name + "_" + str( img_cnt ).zfill( len( str( est_img ) ) ) + ".jpg" ), "JPEG", quality=100 ); # save images to output
                data[ "file" ] = dataset_name + "_" + str( img_cnt ).zfill( len( str( est_img ) ) ) + ".jpg";
                with open( os.path.join( os.getcwd(), output_dir, "annotations", dataset_name + "_" + str( img_cnt ).zfill( len( str( est_img ) ) ) + ".json" ), 'w') as outfile:
                    json.dump( data, outfile, indent=2 )
                img_cnt = img_cnt + 1; # transfer image count

            img.close(); # close image
            progress.display( img_scan, est_img, "Scanning" );


manifest = {};
manifest[ "format" ]  = "HYPE Annotation Format v1.0.0";
manifest[ "name" ]    = dataset_name;
manifest[ "total" ]   = img_scan;
manifest[ "birth" ]   = str( datetime.datetime.now() );
manifest[ "sub_ds" ]  = manifest_list;

with open( os.path.join( os.getcwd(), output_dir, "manifest.json" ), 'w') as outfile:
    json.dump( manifest, outfile, indent=2 )

# Completed
print("\n");
print("Completed: " + str( img_cnt ) + " images Transered of " + str( img_scan ) );
print( "Loss Rate: " + str( img_scan - img_cnt ) );
print( "Transferred to /" + output_dir );
exit();
