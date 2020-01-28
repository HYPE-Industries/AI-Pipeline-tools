# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020
import sys;
import os;
import json;
import requests;
import datetime;
import argparse;
from io import BytesIO
from PIL import Image;
from colored import fg, bg, attr;


# Progress Bar # Vladimir Ignatyev <ya.na.pochte@gmail.com>
def progress(count, total, status=''):
    bar_len = 60;
    filled_len = int( round( bar_len * count / float( total ) ) );
    percents = round( 100.0 * count / float( total ), 1 );
    bar = '=' * filled_len + '-' * ( bar_len - filled_len );
    sys.stdout.write( '[%s] %s%s ...%s\r' % ( bar, percents, '%', status ) );
    sys.stdout.flush();


# Options
parser = argparse.ArgumentParser( description="Dataturk download to HYPE Annotation. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)" );
parser.add_argument( "-i", "--input", type=str, help="Input JSON file. Path to dataturk dataset file." );
parser.add_argument( "-o", "--output", type=str, help="Output directory to create. Directory must not exist. In HYPE Annotations format." );
parser.add_argument( "-n", "--name", type=str, default="awd", help="Dataset prefix name. Prepended to all files exported." );
parser.add_argument( "-d", "--dataset", type=str, default="untitled", help="Dataset name. Full name of dataset for information." );


# Setup all the arguments
args = parser.parse_args();
input_file    = args.input;   # dataturk json file
output_dir    = args.output;  # output folder
dataset_name  = args.name;    # dataset name prefix
dataset_full  = args.dataset; # full name
image_cnt     = 0;            # total images transferred
est_img       = 0;            # estimated images to transfer


# Count Lines of File
file = open( input_file, 'r' )
while 1:
    buffer = file.read(8192*1024)
    if not buffer: break
    est_img += buffer.count('\n')
file.close()


# Start Reading
with open( input_file, 'r' ) as _f:
    print ( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );

    # Create Folder
    try:
        os.mkdir( output_dir );
        os.mkdir( output_dir + "/images" );
        os.mkdir( output_dir + "/annotations" )
    except FileExistsError:
        print( "Directory \'" + output_dir + "\' already exists" );
        exit();

    mod = _f.readline();

    # for each picture
    while mod:
        _file = json.loads( mod.strip() ); # Read line input
        file_name =  dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) );
        file_dir  = output_dir + "/images/" + file_name + ".jpg";

        # Write Image
        response = requests.get( _file[ "content" ] ); # grab from url
        image = Image.open( BytesIO( response.content ) ); # open image
        image.save( file_dir );

        # Write Object File
        data = {}
        data[ "dataset" ] = dataset_full;
        data[ "publisher" ] = "HYPE Industries 2020";
        data[ "file" ] = file_name + ".jpg";
        data[ "date" ] = str( datetime.datetime.now() );
        data[ "annotation" ] = [];
        data[ "size" ] = {};
        if ( _file[ "annotation" ] ):
            data[ "size" ][ "width" ] = _file[ "annotation" ][ 0 ][ "imageWidth" ];
            data[ "size" ][ "height" ] = _file[ "annotation" ][ 0 ][ "imageHeight" ];
        else:
            data[ "size" ][ "width" ] = image.width;
            data[ "size" ][ "height" ] = image.height;

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

        with open( output_dir + "/annotations/" + file_name + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)

        # Next Line
        mod = _f.readline()
        image_cnt += 1
        progress( image_cnt, est_img,"downloading" );


print( "\n " + str( image_cnt ) + " images converted from darkflow (" + input_file + ") to HYPE Annotation format (" + output_dir + ")" );
exit();
