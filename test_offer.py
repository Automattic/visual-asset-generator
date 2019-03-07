import json
import drawBot
import os
from time import sleep
from argparse import ArgumentParser
from random import randint
from offer import Offer
from PIL import Image
from resizeimage import resizeimage

if __name__ == "__main__":
    parser = ArgumentParser(description='drawbot asset generator')
    parser.add_argument('--format', required=False, type=str)
    parser.add_argument('--copy', required=False, type=str)
    parser.add_argument('--offer', required=False, type=str)
    parser.add_argument('--cta', required=False, type=str)
    args = parser.parse_args()

    COLORS = ['_a', '_b', '_c']

    with open('data/templates.json', 'r') as f:
        templates = json.load(f)
        f.close()

    for t in templates:
        if t['name'] == args.format:
            template = t

    homedir = os.environ['HOME']
    try:
        working_dir = '{}/Downloads/renders/{}px'.format(homedir, template['name'])
        os.makedirs(working_dir, exist_ok=True)
    except FileExistsError:
        pass

    ad = Offer(drawBot, template)
    i = 0
    copy = args.copy
    cta = args.cta 
    offer = args.offer

    for c in COLORS:
        frame_path = template['name'] + c + '@2x'
        i+=1
        print('Rendering {} of {}'.format(i, len(COLORS)))
        ad.render(frame_path, copy, cta, offer)
        fp = "{}/Downloads/renders/{}px/{}-{}.png".format(homedir, template['name'], template['name'], 'offer' + c)
        ad.save(fp)
        ad.end()

        # resize the image
        with open(fp, 'r+b') as f:
            with Image.open(f) as img:
                img = Image.open(f)
                img = resizeimage.resize_width(img, int(template['name'].split('_')[0]) * 2)
                img.save(fp + '@2x.png', img.format)
                img = resizeimage.resize_width(img, int(template['name'].split('_')[0]))
                img.save(fp + '@1x.png', img.format)
        os.remove(fp)

    print('Done, assets placed here: {}'.format(working_dir))
