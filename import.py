# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020
import argparse;
import os;
import json;
import requests;
import datetime;
from io import BytesIO
from PIL import Image;
from modules import progress;
from colored import fg, bg, attr;

# Command Line Options
parser = argparse.ArgumentParser( description="Dataturk download to HYPE Annotation. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)" );
parser.add_argument( "-i", "--input", type=str, required=True, help="Location of the file or directory, containing the dataset information." );
parser.add_argument( "-o", "--output", type=str, required=True, help="Output directory name, to create, with HYPE Annotations." );
parser.add_argument( "-f", "--format", type=str, required=True, help="Format to convert from. See documentation to see list of acceptable formats along with their format codes." );
parser.add_argument( "--ds_number", type=str, required=True, help="Dataset number ex. DS1, DS2, DS3" );
parser.add_argument( "--ds_source", type=str, required=True, help="Dataset Source ex. Web Source, Sythetic Data, Web Video, Live Capture, 3D Model" );
parser.add_argument( "--ds_date", type=str, required=True, help="Date the dataset was generated ex. JAN2020, DEC2019" );
parser.add_argument( "--ds_notes", type=str, help="Additional notes to include." );


# Define Varibles
args = parser.parse_args();
input            = args.input;     # input file or directory
output_dir       = args.output;    # output dir to place HYPE Annotations in
format           = args.format;    # format that is being converted from
dataset_number   = args.ds_number; # Dataset Number
dataset_source   = args.ds_source; # Source (ex. Web Source)
dataset_date     = args.ds_date;   # Dataset date
dataset_note     = args.ds_notes;  # add additional notes
images_converted = 0;              # total images converted
images_stack     = 0;              # total images that need converted
label_class_ls   = [];             # list of all class in the annoations


# Varible Implemtation
dataset_name = dataset_number + " " + dataset_date + " - " + dataset_source + " (HAF)"; # Full Dataset Name
input_loc    = os.path.join( os.getcwd(), input ); # Full Input Directory or File
output_loc   = os.path.join( os.getcwd(), output_dir ); # Full Output Directory


# Validate Source Format
if format.lower() not in [ "dataturk", "labelbox", "edgecase" ]:
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


# Create Output Dir
try:
    os.mkdir( output_loc );
    os.mkdir( os.path.join( output_loc + "/images" ) );
    os.mkdir( os.path.join( output_loc + "/annotations" ) );
except:
    print( "Error: An error occured while creating the output directory." );
    exit();


# Manifest Preview
print( "\n" )
print( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );
print( "Convert and download annoations from the " + format + " format to HAF.\n" );
print( "================== information ==================" );
print( "Dataset Name  : " + dataset_name );
print( "Input Format  : " + format );
print( "Input Path    : " + input_loc );
print( "Output Path   : " + output_loc );
print( "\n" );

# Convert
if format == "dataturk":

    # estimated image stack // Import and read lines with the json file
    file = open( input_loc, 'r' )
    while 1:
        buffer = file.read(8192*1024)
        if not buffer: break
        images_stack += buffer.count('\n')
    file.close()


    # Dataturk Converter
    with open( input_loc, 'r' ) as _f:
        _annotation = _f.readline();

        # for each picture (line) in the json file imported
        while _annotation:
            _file     = json.loads( _annotation.strip() ); # Read line input
            file_name = dataset_number + "_" + str( images_converted ).zfill( len( str( images_stack ) ) );
            file_dir  = output_dir + "/images/" + file_name + ".jpg";

            # Download and Write File
            response = requests.get( _file[ "content" ] ); # grab from url
            image = Image.open( BytesIO( response.content ) ); # open image
            image.save( file_dir );

            # Write Object File
            data = {}
            data[ "dataset" ] = {};
            data[ "dataset" ][ "name" ]   = dataset_name;
            data[ "dataset" ][ "number" ] = dataset_number;
            data[ "dataset" ][ "source" ] = dataset_source;

            # Other File Attributes
            data[ "file" ] = file_name + ".jpg";
            data[ "date" ] = str( datetime.datetime.now() );
            data[ "annotation" ] = [];
            data[ "size" ] = {};

            # Set Size of image
            # if ( _file[ "annotation" ] ):
            #     data[ "size" ][ "width" ] = _file[ "annotation" ][ 0 ][ "imageWidth" ];
            #     data[ "size" ][ "height" ] = _file[ "annotation" ][ 0 ][ "imageHeight" ];
            # else:
            data[ "size" ][ "width" ] = image.width;
            data[ "size" ][ "height" ] = image.height;

            # Add all bounding boxes
            if ( _file[ "annotation" ] ):
                for label in _file[ "annotation" ]:
                    data[ "annotation" ].append({
                        'label': label[ "label" ][ 0 ],
                        'bndbox': {
                            'xmin': min( label[ "points" ][ 1 ][ 0 ] * _file[ "annotation" ][0][ "imageWidth" ], label[ "points" ][ 0 ][ 0 ] * _file[ "annotation" ][0][ "imageWidth" ] ),
                            'ymin': min( label[ "points" ][ 0 ][ 1 ] * _file[ "annotation" ][0][ "imageHeight" ], label[ "points" ][ 2 ][ 1 ] * _file[ "annotation" ][0][ "imageHeight" ] ),
                            'xmax': max( label[ "points" ][ 1 ][ 0 ] * _file[ "annotation" ][0][ "imageWidth" ], label[ "points" ][ 0 ][ 0 ] * _file[ "annotation" ][0][ "imageWidth" ] ),
                            'ymax': max( label[ "points" ][ 0 ][ 1 ] * _file[ "annotation" ][0][ "imageHeight" ], label[ "points" ][ 2 ][ 1 ] * _file[ "annotation" ][0][ "imageHeight" ] ),
                        }
                    });

                    # Update list of array
                    if label[ "label" ][ 0 ] not in label_class_ls:
                        label_class_ls.append( label[ "label" ][ 0 ] );

            # Write Annotation File
            with open( os.path.join( output_loc, "annotations", file_name + ".json" ), 'w') as outfile:
                json.dump(data, outfile, indent=2)

            # Next Line
            _annotation = _f.readline()
            images_converted += 1
            progress.display( images_converted, images_stack, "downloading" );

elif format == "labelbox":

    # estimated image stack // Import and read lines with the json file
    with open( input_loc ) as json_file:
        data = json.load( json_file );
        images_stack = len( data );

    # Labelbox Converter
    with open( input_loc ) as json_file:
        data = json.load( json_file );

        for _file in data:
            file_name = dataset_number + "_" + str( images_converted ).zfill( len( str( images_stack ) ) );
            file_dir  = output_dir + "/images/" + file_name + ".jpg";

            # Download and Write File
            response = requests.get( _file[ "Labeled Data" ] ); # grab from url
            image = Image.open( BytesIO( response.content ) ); # open image
            image.save( file_dir );

            # Write Object File
            data = {}
            data[ "dataset" ] = {};
            data[ "dataset" ][ "name" ]   = dataset_name;
            data[ "dataset" ][ "number" ] = dataset_number;
            data[ "dataset" ][ "source" ] = dataset_source;
            data[ "dataset" ][ "label_time" ] = str( _file[ "Seconds to Label" ] ) + "sec";

            # Other File Attributes
            data[ "file" ] = file_name + ".jpg";
            data[ "date" ] = str( datetime.datetime.now() );
            data[ "annotation" ] = [];
            data[ "size" ] = {};

            # Set Size of image
            data[ "size" ][ "width" ] = image.width;
            data[ "size" ][ "height" ] = image.height;


            # Add all bounding boxes
            if ( _file[ "Label" ] ):
                for label in _file[ "Label" ][ "objects" ]:
                    data[ "annotation" ].append({
                        'label': label[ "value" ],
                        'bndbox': {
                            'xmin': label[ "bbox" ][ "left" ],
                            'ymin': label[ "bbox" ][ "top" ],
                            'xmax': label[ "bbox" ][ "left" ] + label[ "bbox" ][ "width" ],
                            'ymax': label[ "bbox" ][ "top" ] + label[ "bbox" ][ "height" ],
                        }
                    });

                    # Update list of array
                    if label[ "value" ] not in label_class_ls:
                        label_class_ls.append( label[ "value" ] );

            # Write Annotation File
            with open( os.path.join( output_loc, "annotations", file_name + ".json" ), 'w') as outfile:
                json.dump( data, outfile, indent=2 )

            # Next Line
            images_converted += 1
            progress.display( images_converted, images_stack, "downloading" );

elif format == "edgecase":

    if os.path.isdir( input_loc ):

    else:
        print( "Error: An error occured while trying to convert. The edgecase format requies and input directory, that is a valid edgecase folder." );

else:
    print( "Error: An error occured while trying to convert. The format was not reconized." );

print( "\nCompleted. " + str( images_converted ) + " images and annotations converted to HAF v1" );

manifest = {};
manifest[ "format" ] = "HYPE Annotation Format v1.0.0";
manifest[ "name" ] = dataset_name;
manifest[ "number" ] = dataset_number;
manifest[ "source" ] = dataset_source;
manifest[ "date" ]   = dataset_date;
manifest[ "total" ]  = images_converted;
manifest[ "birth" ]  = str( datetime.datetime.now() );
manifest[ "class" ]  = label_class_ls;
if dataset_note:
    manifest[ "note" ]  = dataset_note;

with open( os.path.join( output_loc, "manifest.json" ), 'w') as outfile:
    json.dump( manifest, outfile, indent=2 )
