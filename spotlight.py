import numpy as np
import cv2
import json
import drawBot
import sys
from argparse import ArgumentParser
from random import randint

class Spotlight:
    def __init__(self, db, face, template):
        self.db = db
        self.width = template['dimensions']['width']
        self.height = template['dimensions']['height']
        self.spotlight = template['spotlight']
        self.img = { 'path': face['path'], 'w': face['img']['w'], 'h': face['img']['h'] }
        self.face = face['face'] 
        self.logo = template['logo']
        self.frame = template['name']

    # def renderCopy(self):
        # drawBot.fill(1)
        # drawBot.font(RECOLETA, 88)
        # drawBot.blendMode('normal')
        # drawBot.text('Start a hat company.', (100, 350))

    def renderLogo(self):
        logo = self.db.ImageObject('assets/logo_mark.png')
        logo_size = self.db.imageSize(logo)[0]
        sf = self.spotlight['d'] / logo_size
        logo.lanczosScaleTransform(sf)

        self.db.blendMode('normal')
        self.db.image(logo, (self.logo['x'], self.logo['y']))

    def renderFrame(self):
        frame = self.db.ImageObject('assets/{}.png'.format(self.frame))
        # mask = self.db.ImageObject('assets/mask_{}.png'.format(self.mask))
        # frame.blendWithMask(backgroundImage=None, maskImage=mask)
        self.db.blendMode('normal')
        self.db.image(frame, (0,0), .9)

    def renderPortrait(self, magic, shift):
        self.db.fill(1,1,1,1)
        self.db.rect(0,0,self.width, self.height)
        self.spotlight['x'] = self.width * shift

        im = self.db.ImageObject(self.img['path'])
        im.photoEffectMono()
        mask = self.db.ImageObject('assets/mask_fade.png')
        # im.blendWithMask(backgroundImage=None, maskImage=mask)

        #scale the portrait to fit the spotlight
        # print(self.face)
        # print(self.img)
        sf = self.spotlight['d'] / (self.face['w'] / self.img['w'] * self.db.imageSize(im)[0]) * magic 
        # print(sf)
        im.lanczosScaleTransform(sf)
        # print(self.db.imageSize(im))

        # shift the image placement by the difference between where the face starts and where the spotlight is located
        im_x = self.spotlight['x'] - round(self.face['x'] / self.img['w'] * self.db.imageSize(im)[0]) # this line of code took me four hours
        im_y = self.spotlight['y'] - ( self.img['h'] - self.face['h'] - self.face['y'] ) / self.img['h'] * self.db.imageSize(im)[1] # this line of code took me two hours
        # print(im_x, im_y)
        self.db.image(im, (im_x, im_y))
        # self.db.oval(self.spotlight['x'], self.spotlight['y'], 10, 10)

    def render(self, magic, shift):
        self.db.newDrawing()
        self.db.size(self.width, self.height)
        self.renderPortrait(magic, shift)
        self.renderFrame()
        self.renderLogo()

    def save(self, fp):
        print(fp)
        self.db.saveImage(fp)
        
    def end(self):
        self.db.endDrawing()


if __name__ == "__main__":
    parser = ArgumentParser(description='drawbot asset generator')
    parser.add_argument('--format', required=True, type=str)
    args = parser.parse_args()

    RECOLETA = drawBot.installFont('/Users/jeff-ong/Library/Fonts/Latinotype - Recoleta Regular.otf')
    MAGIC = [ .3, .4, .5, .6 ]
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
    ad = Spotlight(drawBot, face, template)
    for magic_number in MAGIC:
        for s in SHIFT:
            ad.render(magic_number, s)
            ad.save("outputs/renders/{}_{}_{}_{}.png".format(templates[0]['name'], face['path'].split('-')[1].split('.')[0], magic_number,s))
            ad.end()
    print('DONE')
    print('\n')

# DIMENSIONS = {
#   'width': 1080,
#   'height': 1080
# }
# SPOTLIGHT = {
#   'x': 700,
#   'y': 420, # 44h
#   'd': 400
#   # 'y': d['height'] * 0.3,
#   # 'd': d['width'] * 0.3636
# }
# LOGO = {
#   'x': 88,
#   'y': 338 
# }
