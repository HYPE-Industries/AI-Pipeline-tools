# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, February 2020

import argparse;
import os;
import json;
import shutil;
from modules import progress;
import xml.etree.cElementTree as ET;
from colored import fg, bg, attr;

# Command Line Options
parser = argparse.ArgumentParser( description="Dataturk download to HYPE Annotation. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)" );
parser.add_argument( "-i", "--input", type=str, required=True, help="Location of the directory of HYPE Annotations, containing the dataset information." );
parser.add_argument( "-o", "--output", type=str, required=True, help="Output directory name, to create, with HYPE Annotations." );
parser.add_argument( "-f", "--format", type=str, required=True, help="Format to convert to. See documentation to see list of acceptable formats along with their format codes." );


# Define Varibles
args = parser.parse_args();
input_dir    = args.input;     # input file or directory
output_dir   = args.output;    # output dir to place HYPE Annotations in
format       = args.format;    # format that is being converted from


# Varible Implemtation
input_loc    = os.path.join( os.getcwd(), input_dir );  # Full Input Directory
output_loc   = os.path.join( os.getcwd(), output_dir ); # Full Output Directory
image_stack  = len( os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ) ); # total images in stack
image_cnt    = 0;  # total images transferred
class_list   = []; # lost of all classes exported

# Open json file manifest
with open( os.path.join( os.getcwd(), input_loc, "manifest.json" ), "r" ) as _manifest:
    manifest     = json.load( _manifest );
    dataset_name = manifest[ "name" ];
    est_img      = manifest[ "total" ];

# Validate Source Format
if format.lower() not in [ "darkflow", "darknet" ]:
    print( "Error: \"" + format.lower() + "\" isn't a valid format. Please take alook at the documentation." );
    exit();


# Validate Input Dir or File
if not os.path.isfile( input_loc ) and not os.path.isdir( input_loc ):
    print( "Error: \"" + input_loc + "\" could not be located as a directory or as a file." );
    exit();


# Validate Output directory doesn't exist
if os.path.isfile( output_loc ) or os.path.isdir( output_loc ):
    print( "Error: \"" + output_loc + "\" is already a path. Please choice a path for a directory that doesn't exist." );
    exit();


# Manifest Preview
print( "\n" )
print( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );
print( "Convert and download annoations from the " + format + " format to HAF.\n" );
print( "================== information ==================" );
print( "Input Format  : " + format );
print( "Input Path    : " + input_loc );
print( "Output Path   : " + output_loc );
print( "\n" );


# Convert
if format == "darkflow":

    # Create Directory
    try:
        os.mkdir( output_dir );
        os.mkdir( output_dir + "/images" );
        os.mkdir( output_dir + "/annotations" );
    except FileExistsError:
        print( "Erro: Directory \'" + output_dir + "\' already exists" );
        exit();

    # convert all
    for manifest in os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ):
        with open( os.path.join( os.getcwd(), input_dir, "annotations", manifest ), "r" ) as _manifest:
            data = json.load( _manifest ) # read file
            img_file = os.path.join( os.getcwd(), input_dir, "images", data[ "file" ] ); # image file

            # Basic
            annotation = ET.Element( "annotation" );
            ET.SubElement( annotation, "folder" ).text = output_dir;
            ET.SubElement( annotation, "filename" ).text = dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".jpg";
            ET.SubElement( annotation, "path" ).text = os.path.basename( output_dir ) + "/" + dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".jpg";

            # Source
            source = ET.SubElement( annotation, "source" );
            ET.SubElement( source, "dataset" ).text = data[ "dataset" ][ "name" ];
            ET.SubElement( source, "publisher").text = "HYPE Industries";
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
            shutil.copyfile( os.path.join( os.getcwd(), input_dir, "images", data[ "file" ] ), os.path.join( os.getcwd(), output_dir, "images", dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".jpg" ) ); # copy image file
            image_cnt = image_cnt + 1;
            progress.display( image_cnt, est_img, "Converting to Darkflow format" ); # update progress

    # Write Classes to file
    with open( os.path.join( os.getcwd(), output_dir, "class.txt" ), "w" ) as txt_file:
        for line in class_list:
            txt_file.write("".join(line) + "\n");

    # copy manifest file over
    if os.path.isfile( os.path.join( os.getcwd(), input_dir, "manifest.json" ) ):
        shutil.copyfile( os.path.join( os.getcwd(), input_dir, "manifest.json" ), os.path.join( os.getcwd(), output_dir, "manifest.json" ) );

elif format == "darknet":
    print( "Format not supported yet. coming soon." )
else:
    print( "Error: An error occured while trying to convert. The format was not reconized." );


print( "\nCompleted. " + str( image_cnt ) + " images and annotations converted from HAF v1 to " + format );
