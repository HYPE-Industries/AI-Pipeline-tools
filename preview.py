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
parser.add_argument( "-p", "--point", help="Enable colored points in label corners.", action="store_true" );
parser.add_argument( "-i", "--input", required=True, help="HYPE Annoation File Path." );

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
    print( "\n" + os.path.join( os.getcwd(), data[ "file" ] ) );
    print( os.path.dirname( os.path.join( os.getcwd(), input_file ) ) );
    print( "\n" + json.dumps( data, indent=2 ) );

    plt.figure( "HYPE Industries Annotation Preview" )
    plt.imshow(im);
    ax = plt.gca()

    for label in data[ "annotation" ]:
        ax.add_patch(patches.Rectangle( (label[ "bndbox" ][ "xmin" ], label[ "bndbox" ][ "ymin" ]), (label[ "bndbox" ][ "xmax" ] - label[ "bndbox" ][ "xmin" ]), (label[ "bndbox" ][ "ymax" ] - label[ "bndbox" ][ "ymin" ]),linewidth=1,edgecolor='r',facecolor='none'));
        plt.text( label[ "bndbox" ][ "xmin" ], label[ "bndbox" ][ "ymax" ] + 20, label[ "label" ], fontsize=8, bbox=dict(facecolor='white') );
        if enable_point:
            plt.scatter( [ label[ "bndbox" ][ "xmin" ] ], [ label[ "bndbox" ][ "ymin" ] ], c="blue" );   # xmin - ymin # top left
            plt.scatter( [ label[ "bndbox" ][ "xmax" ] ], [ label[ "bndbox" ][ "ymin" ] ], c="red" );    # xmax - ymin # top right
            plt.scatter( [ label[ "bndbox" ][ "xmax" ] ], [ label[ "bndbox" ][ "ymax" ] ], c="green" );  # xmax - ymax # bottom right
            plt.scatter( [ label[ "bndbox" ][ "xmin" ] ], [ label[ "bndbox" ][ "ymax" ] ], c="orange" ); # xmin - ymax # bottom left


    plt.xticks([])
    plt.yticks([])
    plt.tight_layout();
    plt.subplots_adjust(bottom=0, left=0)

plt.show()
