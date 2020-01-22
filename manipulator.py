# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020
import json
import os
import argparse;
import sys;
import copy;
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import requests
from io import BytesIO;
from colored import fg, bg, attr;

# Options
parser = argparse.ArgumentParser(description="Generate manupulated copies of images. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)" );
parser.add_argument( "-i", "--input", help="Input directory. Contains `/annotations` and `/img` directories as dictated by HYPE Annotation format. (required)" );
parser.add_argument( "-o", "--output", help="Output directory to create. Directory must not exist. (required)" );
parser.add_argument( "-d", "--dictate", action='store_true', help="Adds notes to annotation file of what process done to pic." );
parser.add_argument( "-n", "--name", default="awd", help="Dataset prefix name. Prepended to all files exported." );

# Setup all the arguments
args           = parser.parse_args();
input_dir      = args.input; # input Directory
output_dir     = args.output; # output directory
dataset_name   = args.name; # dataset name
enable_dictate = args.dictate; # enable notes in annoation
image_cnt      = 0; # total image count
est_img        = 0; # estimated total image after maniputlation


# Progress Bar # Vladimir Ignatyev <ya.na.pochte@gmail.com>
def progress( count, total, status='' ):
    bar_len = 60;
    filled_len = int( round( bar_len * count / float( total ) ) );
    percents = round( 100.0 * count / float( total ), 1 );
    bar = '=' * filled_len + '-' * ( bar_len - filled_len );
    sys.stdout.write( '[%s] %s%s ...%s\r' % ( bar, percents, '%', status ) );
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
    est_img = len( os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ) ) * ( 3 * 7 * 5 );
else:
    print( "Error: Failed to locate. The folders must contain a HYPE annotation format with a /img folder and /annotations folder." );
    exit();

print ( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );


# Open files
for manifest in os.listdir( os.path.join( os.getcwd(), input_dir, "annotations" ) ):
    with open( os.path.join( os.getcwd(), input_dir, "annotations", manifest ), "r" ) as _manifest:
        data = json.load( _manifest ) # read file
        img_file = os.path.join( os.getcwd(), input_dir, "img", data[ "file" ] ); # image file

        if os.path.isfile( img_file ):
            image = Image.open( img_file ); # open file

            for filter in range( 3 ): #3
                _img_filter = image;

                if filter == 0:
                    filter_name = "normal";
                elif filter == 1:
                    filter_name = "black & white";
                    _img_filter = _img_filter.convert( mode='L' );
                elif filter == 2:
                    filter_name = "saturated";
                    saturated = ImageEnhance.Color( _img_filter );
                    _img_filter = saturated.enhance(5);


                for transform in range( 7 ):
                    _img_transform = _img_filter;
                    _width = data[ "size" ][ "width" ];
                    _height = data[ "size" ][ "height" ];
                    _data = copy.deepcopy(data);

                    if transform == 0:
                        transform_name = "normal";
                    elif transform == 1:
                        transform_name = "flip horizontal";
                        _img_transform = _img_transform.transpose( Image.FLIP_LEFT_RIGHT );

                        for label in _data[ "annotation" ]:
                            _xmin,_ymin,_xmax,_ymax = label[ "bndbox" ][ "xmin" ],label[ "bndbox" ][ "ymin" ],label[ "bndbox" ][ "xmax" ],label[ "bndbox" ][ "ymax" ];
                            label[ "bndbox" ][ "xmin" ] = _width - _xmax;
                            label[ "bndbox" ][ "ymin" ] = _ymin;
                            label[ "bndbox" ][ "xmax" ] = _width - _xmin;
                            label[ "bndbox" ][ "ymax" ] = _ymax;

                    elif transform == 2:
                        transform_name = "flip vertical";
                        _img_transform = _img_transform.transpose( Image.FLIP_TOP_BOTTOM );

                        for label in _data[ "annotation" ]:
                            _xmin,_ymin,_xmax,_ymax = label[ "bndbox" ][ "xmin" ],label[ "bndbox" ][ "ymin" ],label[ "bndbox" ][ "xmax" ],label[ "bndbox" ][ "ymax" ];
                            label[ "bndbox" ][ "xmin" ] = _xmin;
                            label[ "bndbox" ][ "ymin" ] = _height - _ymax;
                            label[ "bndbox" ][ "xmax" ] = _xmax;
                            label[ "bndbox" ][ "ymax" ] = _height - _ymin;

                    elif transform == 3:
                        transform_name = "rotate 90";
                        _img_transform = _img_transform.transpose( Image.ROTATE_90 );

                        for label in _data[ "annotation" ]:
                            _xmin,_ymin,_xmax,_ymax = label[ "bndbox" ][ "xmin" ],label[ "bndbox" ][ "ymin" ],label[ "bndbox" ][ "xmax" ],label[ "bndbox" ][ "ymax" ];
                            label[ "bndbox" ][ "xmin" ] = _ymin;
                            label[ "bndbox" ][ "ymin" ] = _width - _xmax;
                            label[ "bndbox" ][ "xmax" ] = _ymax;
                            label[ "bndbox" ][ "ymax" ] = _width - _xmin;

                    elif transform == 4:
                        transform_name = "rotate 180";
                        _img_transform = _img_transform.transpose( Image.ROTATE_180 );

                        for label in _data[ "annotation" ]:
                            _xmin,_ymin,_xmax,_ymax = label[ "bndbox" ][ "xmin" ],label[ "bndbox" ][ "ymin" ],label[ "bndbox" ][ "xmax" ],label[ "bndbox" ][ "ymax" ];
                            label[ "bndbox" ][ "xmin" ] = _width - _xmax;
                            label[ "bndbox" ][ "ymin" ] = _height - _ymax;
                            label[ "bndbox" ][ "xmax" ] = _width - _xmin;
                            label[ "bndbox" ][ "ymax" ] = _height - _ymin;

                    elif transform == 5:
                        transform_name = "rotate 270";
                        _img_transform = _img_transform.transpose( Image.ROTATE_270 );

                        for label in _data[ "annotation" ]:
                            _xmin,_ymin,_xmax,_ymax = label[ "bndbox" ][ "xmin" ],label[ "bndbox" ][ "ymin" ],label[ "bndbox" ][ "xmax" ],label[ "bndbox" ][ "ymax" ];
                            label[ "bndbox" ][ "xmin" ] = _height -_ymax;
                            label[ "bndbox" ][ "ymin" ] = _xmin;
                            label[ "bndbox" ][ "xmax" ] = _height - _ymin;
                            label[ "bndbox" ][ "ymax" ] = _xmax;

                    elif transform == 6:
                        transform_name = "transpose";
                        _img_transform = _img_transform.transpose( Image.TRANSPOSE );

                        for label in _data[ "annotation" ]:
                            _xmin,_ymin,_xmax,_ymax = label[ "bndbox" ][ "xmin" ],label[ "bndbox" ][ "ymin" ],label[ "bndbox" ][ "xmax" ],label[ "bndbox" ][ "ymax" ];
                            label[ "bndbox" ][ "xmin" ] = _ymin;
                            label[ "bndbox" ][ "ymin" ] = _xmin;
                            label[ "bndbox" ][ "xmax" ] = _ymax;
                            label[ "bndbox" ][ "ymax" ] = _xmax;

                    for size in range( 5 ): #6
                        _img_size = _img_transform;

                        if size == 0:
                            size_name = "normal";
                        elif size == 1:
                            size_name = "50%";
                            _img_size = _img_size.resize( ( int( _img_size.width * .5 ), int( _img_size.height * .5 ) ), resample=Image.BILINEAR )
                            _img_size = _img_size.resize( _img_transform.size, Image.NEAREST )
                        elif size == 2:
                            size_name = "40%";
                            _img_size = _img_size.resize( ( int( _img_size.width * .4 ), int( _img_size.height * .4 ) ), resample=Image.BILINEAR )
                            _img_size = _img_size.resize( _img_transform.size, Image.NEAREST )
                        elif size == 3:
                            size_name = "30%";
                            _img_size = _img_size.resize( ( int( _img_size.width * .3 ), int( _img_size.height * .3 ) ), resample=Image.BILINEAR )
                            _img_size = _img_size.resize( _img_transform.size, Image.NEAREST )
                        elif size == 4:
                            size_name = "20%";
                            _img_size = _img_size.resize( ( int( _img_size.width * .2 ), int( _img_size.height * .2 ) ), resample=Image.BILINEAR )
                            _img_size = _img_size.resize( _img_transform.size, Image.NEAREST )


                        # Save File
                        _img_size.save( os.path.join( os.getcwd(), output_dir, "img", dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".jpg" ), "JPEG", quality=60 ); # save images to output
                        _data[ "file" ] = dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".jpg";
                        if enable_dictate:
                            _data[ "note" ] = {};
                            _data[ "note" ][ "filter" ]    = filter_name;
                            _data[ "note" ][ "transform" ] = transform_name;
                            _data[ "note" ][ "size" ]      = size_name;
                        with open( os.path.join( os.getcwd(), output_dir, "annotations", dataset_name + "_" + str( image_cnt ).zfill( len( str( est_img ) ) ) + ".json" ), 'w') as outfile:
                            json.dump(_data, outfile, indent=2);
                        image_cnt = image_cnt + 1;
                        progress( image_cnt, est_img, "Manupulating" );
