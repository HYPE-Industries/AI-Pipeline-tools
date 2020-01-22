# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020
import sys;
import os;
import json;
import argparse;
import shutil;
import xml.etree.cElementTree as ET;
from colored import fg, bg, attr;

# Options
parser = argparse.ArgumentParser(description="Convert to Darkflow format. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)" );
parser.add_argument( "-i", "--input", help="Input directory. Contains `/annotations` and `/img` directories as dictated by HYPE Annotation format. (required)" );
parser.add_argument( "-o", "--output", help="Output directory to create. Directory must not exist. (required)" );
parser.add_argument( "-n", "--name", default="awd", help="Dataset prefix name. Prepended to all files exported." );
parser.add_argument( "-l", "--classlist", help="Return list of all classes as txt", action="store_true" );


# Setup all the arguments
args = parser.parse_args();
input_dir = args.input; # input directory file
output_dir = args.output; # output dir
dataset_name = args.name; # short name for file
enable_class_list = args.classlist; # enable returning class list
class_list = []; # class list
image_cnt  = 0; # total image count
est_img    = 0; # estimated total images


# Progress Bar # Vladimir Ignatyev <ya.na.pochte@gmail.com>
def progress(count, total, status=''):
    bar_len = 60;
    filled_len = int( round( bar_len * count / float( total ) ) );
    percents = round( 100.0 * count / float( total ), 1 );
    bar = '=' * filled_len + '-' * ( bar_len - filled_len );
    sys.stdout.write('[%s] %s%s ...%s\r' % ( bar, percents, '%', status ) );
    sys.stdout.flush();


# Create Directory
try:
    os.mkdir( output_dir );
    os.mkdir( output_dir + "/img" );
    os.mkdir( output_dir + "/annotations" )
except FileExistsError:
    print( "Erro: Directory \'" + output_dir + "\' already exists" );
    exit();


# Validate all inputs
if os.path.isdir( os.path.join( os.getcwd(), input_dir ) ) and os.path.isdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ) and os.path.isdir( os.path.join( os.getcwd(), input_dir, "img" ) ):
    est_img = len( os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ) );
else:
    print( "Error: Failed to locate. The folders must contain a HYPE annotation format with a /img folder and /annotations folder." );
    exit();


print ( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) )

# Open files
for manifest in os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ):
    with open( os.path.join( os.getcwd(), input_dir, "annotations", manifest ), "r" ) as _manifest:
        data = json.load( _manifest ) # read file
        img_file = os.path.join( os.getcwd(), input_dir, "img", data[ "file" ] ); # image file

        # Basic
        annotation = ET.Element( "annotation" );
        ET.SubElement( annotation, "folder" ).text = output_dir;
        ET.SubElement( annotation, "filename" ).text = dataset_name + "_" + str( image_cnt ) + ".jpg";
        ET.SubElement( annotation, "path" ).text = os.path.basename( output_dir ) + "/" + dataset_name + "_" + str( image_cnt ) + ".xml";

        # Source
        source = ET.SubElement( annotation, "source" );
        ET.SubElement( source, "dataset" ).text = data[ "dataset" ];
        ET.SubElement( source, "publisher").text = data[ "publisher" ];
        ET.SubElement( source, "date" ).text = data[ "date" ];

        # Size
        size = ET.SubElement( annotation, "size" );
        ET.SubElement( size, "width" ).text = str( data[ "size" ][ "width" ] );
        ET.SubElement( size, "height" ).text = str( data[ "size" ][ "height" ] );

        # Annotations
        for label in data[ "annotation" ]:
            object = ET.SubElement( annotation, "object" );
            ET.SubElement( object, "name" ).text = label[ "label" ];
            bndbox = ET.SubElement( object, "bndbox" );
            ET.SubElement( bndbox, "xmin" ).text = str( label[ "bndbox" ][ "xmin" ] );
            ET.SubElement( bndbox, "ymin" ).text = str( label[ "bndbox" ][ "ymin" ] );
            ET.SubElement( bndbox, "xmax" ).text = str( label[ "bndbox" ][ "xmax" ] );
            ET.SubElement( bndbox, "ymax" ).text = str( label[ "bndbox" ][ "ymax" ] );


            if not label[ "label" ] in class_list:
                class_list.append( label[ "label" ] )

        tree = ET.ElementTree( annotation )
        tree.write( os.path.join( os.getcwd(), output_dir, "annotations", dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".xml" ) ); # write to file
        shutil.copyfile( os.path.join( os.getcwd(), input_dir, "img", data[ "file" ] ), os.path.join( os.getcwd(), output_dir, "img", dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".jpg" ) ); # copy image file
        image_cnt = image_cnt + 1;
        progress( image_cnt, est_img, "Converting to Darkflow format" ); # update progress


# Write Classes to file
if enable_class_list:
    with open( os.path.join( os.getcwd(), output_dir, "class.txt" ), "w" ) as txt_file:
        for line in class_list:
            txt_file.write("".join(line) + "\n")

# Done
print( "\n " + str( image_cnt ) + " images converted from HYPE Annotation format (" + input_dir + ") to Darkflow format (" + output_dir + ")" );
