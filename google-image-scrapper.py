# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020

from google_images_download import google_images_download;
import requests;
import re;
import os;
import argparse;
import sys;
import json;
import imagehash;
from PIL import Image, ImageMath;
from colored import fg, bg, attr;


# Setup Options
parser = argparse.ArgumentParser( description="Google Image Scrapper for Deep Leaning Pipeline" );
parser.add_argument( "-o", "--output", type=str, help="Output directory. Directory must not exist yet." );
parser.add_argument( "-n", '--num_images', default=100, type=int, help="Number of images to save. Caps at 100." );
parser.add_argument( "-c", '--crosscheck', nargs='*', type=str, help="Crosscheck directories, either dir of images, or hype annotation dir. If nothing, will defualt to all directories. Use \'false\' to disable crosscheck." );
parser.add_argument( "-k", '--keywords', nargs='*', type=str, help="Use specific url from Google." );
parser.add_argument( "-u", '--url', type=str, help="Crosscheck directories, either dir of images, or hype annotation dir. If nothing, will defualt to all directories. Use \'false\' to disable crosscheck." );
parser.add_argument( "-r", '--related_images', action="store_true", help="This argument downloads a ton of images related to the keyword you provided. Google Images page returns list of related keywords to the keyword you have mentioned in the query. This tool downloads images from each of those related keywords based on the limit you have mentioned in your query This argument does not take any value." );
parser.add_argument( "-s", '--similar_images', action="store_true", help="Reverse Image Search or ‘Search by Image’ as it is referred to on Google. Searches and downloads images that are similar to the absolute image link/url you provide." );


# Apply all the arguments
args        = parser.parse_args()
max_img     = args.num_images;     # max amount of images
output_dir  = args.output;         # output directory
crosscheck  = args.crosscheck;     # directories to crosscheck \\ if false disables \\ defaults to all directories
img_hash    = [];                  # list of all images hashes
keywords    = args.keywords;       # keywords to search by
url         = args.url;            # specific url to Search
related_img = args.related_images; # look for related images, be careful \\ keywords only
similar_img = args.similar_images; # give image url and does reverse search \\ url only \\ img url
imgs_succes = 0;                   # total images successfully moved
diff_allowence = 20; # difference between each image; 0 = none; 2 = small; 5 = med; 20 = large

print ( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );


# Create Directory
try:
    os.mkdir( output_dir );
    os.mkdir( output_dir + "/temp" );
except FileExistsError:
    print( "Directory \'" + output_dir + "\' already exists. Moving forward." );



# Predict Error
if ( url and keywords ) :
    print( "Error: You can either use keywords or url. Not both." );
    exit();
elif ( url and related_img ):
    print( "Error: Related Imges can only be used with keywords." );
    exit();
elif ( keywords and similar_img ):
    print( "Error: Similar images can only be used with a url." );
    exit();


# Start Download
response = google_images_download.googleimagesdownload();

if url:
    response.download({
        "url": url,
        "limit": max_img,
        "output_directory": os.path.join( output_dir, "temp" ),
        "no_directory": True,
        "similar_images": similar_img,
        "chromedriver": "chromedriver.exe",
        "socket_timeout": 2
    });
elif len( keywords ) != 0:
    response.download({
        "keywords": ','.join( [ str( elem ) for elem in keywords ] ) ,
        "limit": max_img,
        "output_directory": os.path.join( output_dir, "temp" ),
        "no_directory": True,
        "related_images": related_img,
        "chromedriver": "chromedriver.exe",
        "socket_timeout": 2
    });


# Wait for check the Images
input( "Check to make sure on images located in " + output_dir + "/temp are correct; remove un-wanted images.\nPress enter to merge directories..." );

# get default image directories and convert hype annotations directories
crosscheck_dir = [];

if not crosscheck:
    for dir in os.listdir( os.getcwd() ):
        if ( dir[ 0 ] != "." and os.path.isdir( os.path.join( os.getcwd(), dir ) ) ):
            if os.path.isdir( os.path.join( os.getcwd(), dir, "images" ) ):
                crosscheck_dir.append( os.path.join( dir, "images" ) );
            else:
                crosscheck_dir.append( dir );
else:
    crosscheck_dir.append( output_dir );
    for dir in crosscheck:
        if os.path.isdir( os.path.join( os.getcwd(), dir ) ):
            if os.path.isdir( os.path.join( os.getcwd(), dir, "images" ) ):
                crosscheck_dir.append( os.path.join( dir, "images" ) );
            else:
                crosscheck_dir.append( dir );



print( "Will be crosschecking the following directories..." );
print( crosscheck_dir );

# Hash Images
print( "Hashing images..." );
for dir in crosscheck_dir:
    for file in os.listdir( os.path.join( os.getcwd(), dir ) ):
        if( os.path.isfile( os.path.join( os.getcwd(), dir, file ) ) and file.lower().endswith( ( '.jfif' ) ) == False ):
            img = Image.open( os.path.join( os.getcwd(), dir, file ) );

            # Convert Image Modes
            if img.mode in ('RGBA', 'LA'):
                background = Image.new(img.mode[:-1], img.size, "#000")
                background.paste(img, img.split()[-1])
                img = background
            elif img.mode == 'P':
                img = img.convert( "RGB" );

            img_hash.append( imagehash.average_hash( img ) );


# move new images
for file in os.listdir( os.path.join( os.getcwd(), output_dir, "temp" ) ):
    if( os.path.isfile( os.path.join( os.getcwd(), output_dir, "temp", file ) ) and file.lower().endswith( ( '.jfif' ) ) == False ):
        try:
            img = Image.open( os.path.join( os.getcwd(), output_dir, "temp", file ) );

            # Convert Image Modes
            if img.mode in ('RGBA', 'LA'):
                background = Image.new(img.mode[:-1], img.size, "#000")
                background.paste(img, img.split()[-1])
                img = background
            elif img.mode == 'P':
                img = img.convert( "RGB" );

            # Check for Duplicated Images
            hash = imagehash.average_hash( img );
            _exists = False;
            for _h in img_hash:
                if abs( hash - _h ) <= diff_allowence:
                    _exists = True;

            # save if doesn't exist
            if not _exists:
                img_hash.append( hash );
                img.save( os.path.join( output_dir,  str( hash ) + ".jpg" ), "JPEG", quality=100 ); # save images to output
                os.remove( os.path.join( os.getcwd(), output_dir, "temp", file ) );
                imgs_succes = imgs_succes + 1;

            img.close();
        except:
            print("failed")
            # do nothing

print( "Images in temp folder can now be deleted, as they are duplications." );
print( "Images successfully added: " + str( imgs_succes ) );
