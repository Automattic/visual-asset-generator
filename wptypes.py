import json
import drawBot
import os
from time import sleep
from argparse import ArgumentParser
from random import randint
from PIL import Image
from resizeimage import resizeimage
from random import randint
from offer_spotlight import OfferSpotlight

with open('data/templates.json', 'r') as f:
    templates = json.load(f)
    f.close()

with open('data/types.json', 'r') as f:
    wp_types = json.load(f)
    f.close()
    
with open('data/dotcom_faces.json', 'r') as f:
    faces = json.load(f)
    f.close()

template = templates[0]
homedir = os.environ['HOME']
try:
    working_dir = '{}/Downloads/renders/{}px'.format(homedir, template['name'])
    os.makedirs(working_dir, exist_ok=True)
except FileExistsError:
    pass

i = 0
ad = OfferSpotlight(drawBot, template)

COLORS = ['_a', '_b', '_c']
copy = wp_types[2]['headline']
cta = "Learn more"

for t in wp_types[2]['data']: 
    c = COLORS[randint(0,2)]
    frame_path = template['name'] + c + '@2x'
    face = faces[randint(0,len(faces) - 1)]
    ad.render(frame_path, face, copy, cta, t)
    fp = "{}/Downloads/renders/{}px/{}-{}.png".format(homedir, template['name'], template['name'], str(t).split(" ")[0])
    ad.save(fp)
    ad.end()

    # resize the image
    with open(fp, 'r+b') as f:
        with Image.open(f) as img:
            img = Image.open(f)
            img = resizeimage.resize_width(img, int(template['name'].split('_')[0]) * 2)
            img.save(fp + '@2x.png', img.format)
    os.remove(fp)
