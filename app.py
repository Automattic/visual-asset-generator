import json
import drawBot
import os
from argparse import ArgumentParser
from random import randint
from spotlight import Spotlight
# from googletrans import Translator

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', ''):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    parser = ArgumentParser(description='drawbot asset generator')
    parser.add_argument('--format', required=True, type=str)
    parser.add_argument('--copy', required=False, type=str)
    parser.add_argument('--translate', type=str2bool, const=True, help="Translate the copy.", nargs='?')
    args = parser.parse_args()

    MAGIC = [ .5, .6 ]
    LANGUAGES = ['en']
    COLORS = ['_a', '_b', '_c']
    SIZES = ['', '@2x']
    if args.translate:
        LANGUAGES = ['en', 'es', 'ja']

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
    homedir = os.environ['HOME']
    try:
        print('Making directory {}/Downloads/renders/{}'.format(homedir, img_id))
        os.makedirs('{}/Downloads/renders/{}'.format(homedir, img_id), exist_ok=True)
    except FileExistsError:
        pass

    ad = Spotlight(drawBot, face, template)
    i = 0
    retina = False
    copy = args.copy
    cta = "Start for free"
    # translator = Translator()
    # for language in LANGUAGES:
    #     copy = translator.translate(args.copy, dest=language).text
    #     cta = translator.translate("Start for free", dest=language).text
    for s in SIZES:
        for c in COLORS:
            frame_path = template['name'] + c + s
            for magic_number in MAGIC:
                i+=1
                print('Rendering {} of {}'.format(i, len(MAGIC) * len(SIZES) * len(COLORS) * len(LANGUAGES)))
                if s == '@2x' and retina == False:
                    ad.renderRetina()
                    retina = True
                ad.render(magic_number, frame_path, copy, cta)
                ad.save("{}/Downloads/renders/{}/{}_{}_{}.png".format(homedir, img_id, 'en', frame_path, magic_number))
                ad.end()
    print('Done.')
