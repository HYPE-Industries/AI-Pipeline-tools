# Deep Learning Pipeline
# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
# Written by Evan Sellers <sellersew@gmail.com>, January 2020

# FIXME

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import argparse
import sys
import json

def get_soup( url, header ):
    return BeautifulSoup( urllib2.urlopen( urllib2.Request( url,headers=header ) ), "html.parser" );

def main(args):
    # Options
    parser = argparse.ArgumentParser( description="Google Image Scrapper for Deep Leaning Pipeline" );
    parser.add_argument( "-i", "--input", type=str, help="Input URL to scrap." );
    parser.add_argument( "-o", "--output", type=str, help="Output directory. Directory must not exist yet." );
    parser.add_argument( "-n", '--num_images', default=100, type=int, help="Number of images to save. Caps at 100." );

    # Setup all the arguments
    args       = parser.parse_args()
    url        = args.input;         # input url
    max_img    = args.num_images;    # max amount of images
    outpur_dir = args.output;        # output directory

    # attr
    image_type="Action"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    ActualImages=[]# contains the link for Large original images, type of  image

    # Generate List of Images
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link, Type = json.loads( a.text )[ "ou" ], json.loads( a.text )[ "ity" ];
        ActualImages.append( ( link, Type ) );

    # Download Images
    for i, (img , Type) in enumerate( ActualImages[0:max_images]):
        try:
            req = urllib2.Request(img, headers={'User-Agent' : header})
            raw_img = urllib2.urlopen(req).read()
            if len( Type )==0:
                f = open( os.path.join( os.getcwd(), outpur_dir , "img" + "_"+ str(i) + ".jpg"), 'wb' );
            else :
                f = open( os.path.join( os.getcwd(), outpur_dir , "img" + "_" + str(i) + "." + Type), 'wb' );
            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : "+img
            print e



# Dat's Funny
