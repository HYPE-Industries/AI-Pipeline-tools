# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, February 2020

import imagehash;
import os
from PIL import Image, ImageMath;

def image( image_dir ):
    if os.path.isfile( image_dir ):
        try:
            img = Image.open( image_dir );

            # Convert Image Modes
            if img.mode in ('RGBA', 'LA'):
                background = Image.new(img.mode[:-1], img.size, "#000")
                background.paste(img, img.split()[-1])
                img = background
            elif img.mode == 'P':
                img = img.convert( "RGB" );

            return str( imagehash.average_hash( img ) );
        except:
            return False;
    else:
        return False;
