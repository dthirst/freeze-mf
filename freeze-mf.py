#!/usr/bin/env python3

# freeze-mf - tool for making montages of cryoEM screening images
# written 2022 by demian keihsler at the institute of molecular pathology, vienna
# ********
# usage:
#   save the files you want to mount in the following pattern in one folder:
#       <name>_map.<ext>,
#       <name>_square.<ext>, 
#       <name>_hole.<ext>, 
#       <name>_i1.<ext>, 
#       <name>_i2.<ext>
#   start the script by writing 'python3 <path-to-script>/freeze.mf -p <path-of-files>'
#   the montages will be save in the same folder with the pattern <name)>_montage.png
#   thank your local technician
# ********

import argparse
from PIL import Image, ImageDraw
from os import path, listdir
from math import floor

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='Path to the directory containing your images.', required=True)
parser.add_argument('-w', '--width', help='Width in px of the montage.', default=1600)
parser.add_argument('-m', '--margin', help='Margin as decimal fraction (eG. 0.05 for 5% margin).', default=0.05)
args = vars(parser.parse_args())

width = args['width']
height = floor(width / 2)
margin_frac = args['margin']
dirpath = args['path']


def resize_to_fraction(image, fraction, margin):
    size = (floor(width / fraction) - 2 * margin,
            floor(width / fraction) - 2 * margin)
    return image.resize(size)

def load_images(src):
    images = {}
    filenames = listdir(src)
    
    for file in [ st for st in filenames if 'map' in st ]:
        image = Image.open(path.join(src, file))
        images[file.split('map')[0]] = [ image, None, None, None, None ]
    for file in listdir(src):
        try:
            image = Image.open(path.join(src, file))
            if 'square' in file:
                images[file.split('square')[0]][1] = image 
            elif 'hole' in file:
                images[file.split('hole')[0]][2] = image
            elif 'i1' in file:
                images[file.split('i1')[0]][3] = image
            elif 'i2' in file:
                images[file.split('i2')[0]][4] = image
        except IOError:
            pass
    return images

def main():
    imagesets = load_images(dirpath)

    for fname, images in imagesets.items():
        montage = Image.new(mode='RGBA', size=(width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(montage)
        montage.paste('black', (0,0,width,height))
        margin = floor(margin_frac * width / 2)
        montage.paste(resize_to_fraction(images[0], 2, margin), (margin, margin))

        for i, image in enumerate(images[1:]):
            if image is None:
                break
            resized = resize_to_fraction(image, 4, margin)

            xpos = floor(width / 2) + (i > 1) * floor(width / 4)
            ypos = floor(height / 2) * (i % 2)

            montage.paste(resized, (xpos + margin, ypos + margin))
        montage.save(path.join(dirpath, f'{fname}_montage.png'))

if __name__ == '__main__':
    main()
