#!/usr/bin/env python3

# freeze-mf - a simple tool for making montages of cryoEM screening images
# written 2022 by demian keihsler at the institute of molecular pathology, vienna
# ********
# usage:
#   - save the files you want to mount in the following pattern in one folder:
#       <name>_map.<ext>,
#       <name>_square.<ext>, 
#       <name>_hole.<ext>, 
#       <name>_i1.<ext>, 
#       <name>_i2.<ext>
#   - you can have as many different groups of files as you want, as long as files that belong together
#     always start with the same name and have the same extension. the script will iterate through the 
#     folder and make a montage for each group that has at least a file whose name ends with _map.
#   - start the script by writing 'python3 <path-to-script>/freeze.mf -p <path-of-files>'
#   - the montages will be save in the same folder with the naming pattern <name>_montage.png
#   - please mind the following expected behaviour: 
#     - if you have a map file but no square and smaller, the montage will contain only the map. same for
#       square but no hole, hole but no i1/i2.
#     - if you have a square and/or any other file but no map, there will be no montage.
#   thank your local technician 🍻
# ********

import argparse
from PIL import Image, ImageDraw
from os import path, listdir
from math import floor

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='Path to the directory containing your images.', required=True)
parser.add_argument('-w', '--width', help='Width in px of the montage.', default=1600)
parser.add_argument('-m', '--margin', help='Margin as decimal fraction (eG. 0.05 for 5% margin).', default=0.05)
parser.add_argument('-c', '--color', help='Background color as rgb value (eG. 255 255 255 for white)',
                    nargs='+', default=[0,0,0], type=int)
args = vars(parser.parse_args())

width = args['width']
height = floor(width / 2)
margin_frac = args['margin']
dirpath = args['path']
bgcolor = tuple(args['color'])

def resize_to_fraction(image, fraction, margin):
    size = (floor(width / fraction) - 2 * margin,
            floor(width / fraction) - 2 * margin)
    return image.resize(size)

def check_and_open(src, fbasename, fext, label):
    try:
        image = Image.open(path.join(src, f'{fbasename}{label}{fext}'))
        return image
    except:
        return None

def load_images(src):
    print('- loading images...')
    images = {}
    filenames = listdir(src)
    
    for file in [ st for st in filenames if 'map' in st ]:
        image = Image.open(path.join(src, file))
        fbasename, fext = file.split('map')
        cleanext = fext.split('.')[1]
        fext = f'.{cleanext}'
        images[fbasename] = [ image, None, None, None, None ]

        images[fbasename][1] = check_and_open(src, fbasename, fext, 'square')
        images[fbasename][2] = check_and_open(src, fbasename, fext, 'hole')
        images[fbasename][3] = check_and_open(src, fbasename, fext, 'i1')
        images[fbasename][4] = check_and_open(src, fbasename, fext, 'i2')
    print('- done.')
    return images

def main():
    imagesets = load_images(dirpath)
    print('mounting images...')
    for fname, images in imagesets.items():
        montage = Image.new(mode='RGBA', size=(width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(montage)
        montage.paste(bgcolor, (0,0,width,height))
        margin = floor(margin_frac * width / 2)
        montage.paste(resize_to_fraction(images[0], 2, margin), (margin, margin))

        for i, image in enumerate(images[1:]):
            if image is None:
                break
            resized = resize_to_fraction(image, 4, margin)

            xpos = floor(width / 2) + (i > 1) * floor(width / 4)
            ypos = floor(height / 2) * (i % 2)

            montage.paste(resized, (xpos + margin, ypos + margin))
        montage.save(path.join(dirpath, f'{fname}montage.png'))
        print(f'{fname}montage.png saved.')

if __name__ == '__main__':
    main()
