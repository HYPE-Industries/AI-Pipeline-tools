# Deep Learning Pipeline
# Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, January 2020

import matplotlib.pyplot as plt;
import matplotlib.patches as patches
import sys;
import os;
import json;
import argparse;
import numpy as np
from PIL import Image;
from colored import fg, bg, attr;

# options
parser = argparse.ArgumentParser( description="Point Plot Preview HYPE Annotation. Copyright (C) HYPE Industries Cloud Services Division - All Rights Reserved (HYPE-CSD)" )
parser.add_argument( "-p", "--point", help="Show corner points as colors", action="store_true" );
parser.add_argument( "-i", "--input", help="Input JSON file. Path to HYPE Annotation file." );

# Setup all the arguments
args = parser.parse_args();
input_file = args.input; # input json file
enable_point = args.point; # enable corner points

os.chdir( os.path.dirname( os.path.join( os.getcwd(), input_file ) ) ); # change Directory to one containing json
os.chdir( "../images" );

print ( '%s%s HYPE Industries Military Defense Division - PRISM Mainframe %s' % ( fg( 255 ), bg( 9 ), attr( 0 ) ) );

with open( os.path.join( os.getcwd(), input_file ), "r" ) as read_file:
    data = json.load( read_file ) # read file
    im = np.array( Image.open( os.path.join( os.getcwd(), data[ "file" ] ) ), dtype=np.uint8 ); # open image
    fig,ax = plt.subplots( 1 ); # Create figure and axes
    ax.imshow(im); # Display the image

    for label in data[ "annotation" ]:
        ax.add_patch(patches.Rectangle( (label[ "bndbox" ][ "xmin" ], label[ "bndbox" ][ "ymin" ]), (label[ "bndbox" ][ "xmax" ] - label[ "bndbox" ][ "xmin" ]), (label[ "bndbox" ][ "ymax" ] - label[ "bndbox" ][ "ymin" ]),linewidth=1,edgecolor='r',facecolor='none'));
        if enable_point:
            plt.scatter( [ label[ "bndbox" ][ "xmin" ] ], [ label[ "bndbox" ][ "ymin" ] ], c="blue" );   # xmin - ymin # top left
            plt.scatter( [ label[ "bndbox" ][ "xmax" ] ], [ label[ "bndbox" ][ "ymin" ] ], c="red" );    # xmax - ymin # top right
            plt.scatter( [ label[ "bndbox" ][ "xmax" ] ], [ label[ "bndbox" ][ "ymax" ] ], c="green" );  # xmax - ymax # bottom right
            plt.scatter( [ label[ "bndbox" ][ "xmin" ] ], [ label[ "bndbox" ][ "ymax" ] ], c="orange" ); # xmin - ymax # bottom left


plt.show()
