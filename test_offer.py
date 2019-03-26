import json
import drawBot
import os
from argparse import ArgumentParser
from random import randint
from offer import Offer
from PIL import Image
from resizeimage import resizeimage

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', ''):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    parser = ArgumentParser(description='drawbot asset generator')
    parser.add_argument('--format', required=False, type=str)
    parser.add_argument('--copy', required=False, type=str)
    parser.add_argument('--offer', required=False, type=str)
    parser.add_argument('--cta', required=False, type=str)
    parser.add_argument('--spotlight', type=str2bool, const=False, help="Use a portrait", nargs='?')
    args = parser.parse_args()

    COLORS = ['_a', '_b', '_c']

    with open('data/templates.json', 'r') as f:
        templates = json.load(f)
        f.close()

    with open('data/faces.json', 'r') as f:
        faces = json.load(f)
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

    ad = Offer(drawBot, template, args.spotlight)
    i = 0

    for c in COLORS:
        frame_path = template['name'] + c + '@2x'
        face = faces[randint(0,len(faces) - 1)] # pick a random portrait to use
        i+=1
        print('Rendering {} of {}'.format(i, len(COLORS)))
        ad.render(frame_path, face, args.copy, args.cta, args.offer)
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
