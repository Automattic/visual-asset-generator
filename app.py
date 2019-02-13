import json
import drawBot
import os
from argparse import ArgumentParser
from random import randint
from spotlight import Spotlight

if __name__ == "__main__":
    parser = ArgumentParser(description='drawbot asset generator')
    parser.add_argument('--format', required=True, type=str)
    parser.add_argument('--copy', required=False, type=str)
    args = parser.parse_args()

    MAGIC = [ .4, .5, .6 ]
    SHIFT = [ .6, .625, .65 ]

    with open('data/faces.json', 'r') as f:
        faces = json.load(f)
        f.close()

    with open('data/templates.json', 'r') as f:
        templates = json.load(f)
        f.close()

    for t in templates:
        if t['name'] == args.format:
            template = t

    face = faces[randint(0,len(faces) - 1)]
    img_id = face['path'].split('-')[1].split('.')[0]
    try:
        print('Making directory outputs/renders/{}'.format(img_id))
        os.mkdir('outputs/renders/{}'.format(img_id))
    except:
        print('Directory exists, continuing...')


    ad = Spotlight(drawBot, face, template, args.copy)
    i = 0
    for magic_number in MAGIC:
        i+=1
        print('Rendering image {} of {}'.format(i, len(MAGIC) * 2))
        ad.render(magic_number, 1)
        ad.save("outputs/renders/{}/{}_{}.png".format(img_id, template['name'], magic_number))
        ad.end()

    template['name'] = template['name'] + '@2x'
    ad = Spotlight(drawBot, face, template, args.copy)
    for magic_number in MAGIC:
        i+=1
        print('Rendering image {} of {}'.format(i, len(MAGIC) * 2))
        ad.render(magic_number, 1)
        ad.save("outputs/renders/{}/{}_{}.png".format(img_id, template['name'], magic_number))
        ad.end()
    print('Done.')
