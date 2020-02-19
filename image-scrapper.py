# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020

# FIXME Implemtation keywords => https://github.com/HYPE-Industries/AI-Pipeline-tools/blob/43f81101e3c0b4ba9396278f0740a47c6559f5c2/google-image-scrapper.py

import argparse;
import os;
from modules import crosscheck;
from colored import fg, bg, attr;
# from google_images_download import google_images_download;
from modules import google_images_download;

# Setup Options
parser = argparse.ArgumentParser( description="Google Image Scrapper for Deep Leaning Pipeline" );
parser.add_argument( "-o", "--output", type=str, required=True, help="Output directory name, with downloaded images." );
parser.add_argument( "-n", '--num_images', default=100, type=int, help="Number of images to download to directory." );
parser.add_argument( "-c", '--crosscheck', nargs='*', type=str, help="Crosscheck directories, either dir of images, or hype annotation dir. If nothing, will defualt to all directories. Use \'-1\' to disable crosscheck." );
parser.add_argument( "-u", '--url', type=str, required=True, help="Google Image URL will be scrapped for images." );


# Apply all the arguments
args          = parser.parse_args();
image_max     = args.num_images; # max amount of images
output        = args.output;     # output directory
url           = args.url;        # google url to scrap
_crosscheck   = args.crosscheck; # directories to crosscheck \\ if false disables \\ defaults to all directories
image_hash    = [];              # list of image hashes
image_count   = 0;               # total new images download
image_success = 0;               # total images successfully transferred


# Varible Implemtation
output_loc = os.path.join( os.getcwd(), output ); # Full Output Directory


# Create Output directory
try:
    os.mkdir( output_loc );
    os.mkdir( os.path.join( output_loc, "temp" ) );
except FileExistsError:
    # Directory already exist do nothing
    print( "Directory already exists... Continuing Process" );


# Cross Check Locations
crosscheck_loc = [];
if not _crosscheck:
    # if no directories set grab one from main directory of repo
    for dir in os.listdir( os.getcwd() ):
        if ( dir[ 0 ] != "." and os.path.isdir( os.path.join( os.getcwd(), dir ) ) ):
            if os.path.isdir( os.path.join( os.getcwd(), dir, "images" ) ):
                crosscheck_loc.append( os.path.join( os.getcwd(), dir, "images" ) );
            else:
                crosscheck_loc.append( os.path.join( os.getcwd(), dir ) );
elif _crosscheck[ 0 ] == "-1":
    # Disabled Crosscheck
    print( "Crosscheck disabled" );
else:
    # Check for valid directories & Check for HAF
    crosscheck_loc.append( output_dir );
    for dir in _crosscheck:
        if os.path.isdir( os.path.join( os.getcwd(), dir ) ):
            if os.path.isdir( os.path.join( os.getcwd(), dir, "images" ) ):
                crosscheck_loc.append( os.path.join( os.getcwd(), dir, "images" ) );
            else:
                crosscheck_loc.append( os.getcwd(), dir );


# Manifest Preview
print( "\n" )
print( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );
print( "Downloading images from google and crosschecking.\n" );
print( "================== information ==================" );
print( "URL            : " + url );
print( "Total Image    : " + str( image_max ) );
print( "Output Path    : " + output_loc );
if len( crosscheck_loc ) != 0:
    print( "Crosscheck Dir : " );
    for dir in crosscheck_loc:
        print( "  └ " + dir );
else:
    print( "Crosscheck Dir : DISABLED" );
print( "\n" );


# Start Download
response = google_images_download.googleimagesdownload();
response.download({
    "url": url,
    "limit": image_max,
    "no_directory": True,
    "output_directory": os.path.join( output_loc, "temp" ),
    "chromedriver": "./modules/chromedriver.exe",
});


# Generate CrossCheck Codes
print( "Hashing images..." );
if len( crosscheck_loc ) != 0:
    for dir in crosscheck_loc:
        for file in os.listdir( dir ):
            if os.path.isfile( os.path.join( dir, file ) ):
                image_hash.append( crosscheck.image( os.path.join( dir, file ) ) );


# Crosscheck Images Downloaded
print( "Crosschecking downloaded images..." );
for file in os.listdir( os.path.join( output_loc, "temp" ) ):
    if os.path.isfile( os.path.join( output_loc, "temp", file ) ):
        if crosscheck.image( os.path.join( output_loc, "temp", file ) ) in image_hash:
            os.remove( os.path.join( output_loc, "temp", file ) );
        else:
            image_hash.append( crosscheck.image( os.path.join( output_loc, "temp", file ) ) );
            image_count += 1;


# Approve Images
print( str( image_count ) + " Images have been download to a tempary directory. Please verify all of the images are up to specification. Images will be transfer out of temp and into root, after pressing enter." );
print( "Temp Dir:" + os.path.join( output_loc, "temp" ) + "\n" );
input( '%s%s Press [ ENTER ] to continue... %s' % ( fg( 255 ), bg( 27 ), attr( 0 ) )  )


# Move Images
print( "Transferring Images..." );
for file in os.listdir( os.path.join( output_loc, "temp" ) ):
    if os.path.isfile( os.path.join( output_loc, "temp", file ) ):
        os.replace( os.path.join( output_loc, "temp", file ), os.path.join( output_loc, file ) );
        image_success += 1;

# Process Complete
print( "Process complete. " + str( image_success ) + " successfully transferred.");
