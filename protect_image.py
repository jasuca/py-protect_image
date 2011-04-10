#!/usr/bin/env python
# encoding: utf-8
"""
protect_image.py

Created by Jacob Sunol (www.jasuca.com)
Licenced under MIT Licence (http://opensource.org/licenses/mit-license.php)

Test image from wWikimedia.org - http://commons.wikimedia.org/wiki/File:Turbinella_pyrum_01.jpg
"""

import sys
import os

import Image
import random

def split_y(size_y, divisions):
    """
    Split into x divisions a y size
    """
    inc = size_y / divisions
    return [inc*(x+1) for x in range(divisions)]
    
def generate_boxes(size_x, size_y, divisions=4):
    """
    Generate n boxes full x size
    """
    y_splited = split_y(size_y, divisions)
    boxes = []
    y_top = 0
    for y_bottom in y_splited:
        boxes.append((0,y_top, size_x, y_bottom))
        y_top = y_bottom
    return boxes
    
def main():
    """
    Constants
    """
    divisions = 5
    infile = 'test_in.png'
    outfile = 'test_out.png'
    htmloutfile = outfile + '.html'
    format_file = 'PNG'

    #Open the image
    im = Image.open(infile)
    size_x, size_y = im.size
    
    #Generate the boxes for the image
    boxes = generate_boxes(size_x, size_y, divisions)
    
    #Crop the image
    regions = []
    for box in boxes:
        region = im.crop(box)
        regions.append(region)

    #Shuffle the boxes croped
    random.shuffle(boxes)

    #Create a new image
    im_new = Image.new(im.mode, im.size)
    
    #Paste the croped parts
    for x in range(len(boxes)):
        box = boxes[x]
        region = regions[x]
        #print box, region
        im_new.paste(region, box)
    
    #Save the new image
    im_new.save(outfile, format_file, quality=100)

    #Generate the new HTML file
    f = open(htmloutfile,'w')
    f.write('<html><head></head><body>')
    for box in boxes:
        f.write("<div style=\"\
                background: url('%s') no-repeat center top; \
                background-position: %0.2fpx -%0.2fpx; \
                width: %0.2fpx; \
                height:%0.2fpx;\
                \"></div>"%(outfile, box[0], box[1], size_x, size_y/divisions ))
    f.write('</body></html>')
    f.close()
    
    pass

if __name__ == '__main__':
    main()

