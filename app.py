import json
import drawBot
import os
from argparse import ArgumentParser
from random import randint
from spotlight import Spotlight
from googletrans import Translator

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    parser = ArgumentParser(description='drawbot asset generator')
    parser.add_argument('--format', required=True, type=str)
    parser.add_argument('--copy', required=False, type=str)
    parser.add_argument('--translate', default="true", type=str2bool, const=True, help="Translate the copy.", nargs='?')
    args = parser.parse_args()
    translator = Translator()

    MAGIC = [ .5, .6 ]
    LANGUAGES = ['en', 'es', 'ja']
    COLORS = ['_a', '_b', '_c']
    SIZES = ['', '@2x']

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

    ad = Spotlight(drawBot, face, template)
    i = 0
    doubled = False
    for language in LANGUAGES:
        copy = translator.translate(args.copy, dest=language).text
        for s in SIZES:
            for c in COLORS:
                frame_path = template['name'] + c + s
                for magic_number in MAGIC:
                    i+=1
                    print('Rendering image {} of {}'.format(i, len(MAGIC) * len(SIZES) * len(COLORS) * len(LANGUAGES)))
                    if s == '@2x' and doubled == False:
                        ad.doubleSize()
                        doubled = True
                    ad.render(magic_number, frame_path, copy)
                    ad.save("outputs/renders/{}/{}_{}_{}.png".format(img_id, language, frame_path, magic_number))
                    ad.end()
    print('Done.')
