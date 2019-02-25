from roundedRect import roundedRect
from random import shuffle

LOREM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

class Spotlight:
    def __init__(self, db, face, template):
        self.noto = db.installFont('assets/NotoSans-Regular.ttf')
        self.recoleta = db.installFont('assets/Latinotype - Recoleta Regular.otf')
        self.db = db
        self.content = template['content']
        self.button = { 'fontSize': 12, 'width': 124, 'height': 40, 'borderRadius': 3 }
        self.width = template['dimensions']['width']
        self.height = template['dimensions']['height']
        self.spotlight = template['spotlight']
        self.img = { 'path': face['path'], 'w': face['img']['w'], 'h': face['img']['h'] }
        self.face = face['face'] 
        self.logo = template['logo']
        self.color_scheme = 'blue'
        self.db.stroke(None)
        # self.frame = template['frame']
        self.margin = self.width * .1
        if (self.height < self.width):
            self.margin = self.height * .1

    def renderCopy(self, cursor):
        self.db.fill(1)
        self.db.font(self.recoleta, self.content['fontSize'])
        copy_x = self.margin
        copy_y = cursor - (self.margin / 2) - self.content['textBox']['height']
        self.db.textBox(self.copy, (copy_x, copy_y, self.content['textBox']['width'], self.content['textBox']['height']))
        cursor = copy_y 
        return cursor
    
    def renderButton(self, cursor):
        self.db.blendMode('normal')
        self.db.fill(213/255,44/255,130/255) # product pink
        if self.color_scheme == 'pink': 
            self.db.fill(1/255,96/255,135/255) # product blue
        button_y = cursor - (self.margin / 2) - self.button['height']
        button_x = self.margin 
        roundedRect(self.db, button_x, button_y, self.button['width'], self.button['height'], self.button['borderRadius'])
        self.db.font('Noto Sans Bold')
        self.db.fontSize(self.button['fontSize'])
        self.db.fill(1) # product pink
        self.db.textBox(self.cta, (button_x, button_y - self.button['height'] / 3.5, self.button['width'], self.button['height']), align="center")
        cursor -= self.button['height']
        return cursor

    def renderBadge(self, cursor):
        badge = self.db.ImageObject('assets/badge.png')
        badge_size = self.db.imageSize(badge)[0]
        sf = self.button['width'] / badge_size
        badge.lanczosScaleTransform(sf)

        badge_y = cursor - self.db.imageSize(badge)[1] - self.margin
        badge_x = self.margin
        self.db.blendMode('normal')
        self.db.image(badge, (badge_x, badge_y))
        return badge_y

    def renderLogo(self):
        logo = self.db.ImageObject('assets/logo_mark_gray.png')
        logo_size = self.db.imageSize(logo)[0]
        sf = self.spotlight['d'] / logo_size
        logo.lanczosScaleTransform(sf)

        self.db.blendMode('multiply')
        self.db.image(logo, (self.logo['x'], self.logo['y']))

    def renderFrame(self, frame_path):
        frame = self.db.ImageObject('assets/{}.png'.format(frame_path))
        frame_size = self.db.imageSize(frame)[0]
        sf = self.width / frame_size
        frame.lanczosScaleTransform(sf)
        # mask = self.db.ImageObject('assets/mask_{}.png'.format(self.mask))
        # frame.blendWithMask(backgroundImage=None, maskImage=mask)
        self.db.blendMode('multiply')
        self.db.image(frame, (0,0))

    def renderPortrait(self, magic):
        self.db.fill(1,1,1,1)
        self.db.rect(0,0,self.width, self.height)
        # self.spotlight['x'] = self.width * shift

        im = self.db.ImageObject(self.img['path'])
        im.photoEffectMono()
        # mask = self.db.ImageObject('assets/mask_fade.png')
        # im.blendWithMask(backgroundImage=None, maskImage=mask)

        #scale the portrait to fit the spotlight
        sf = self.spotlight['d'] / (self.face['w'] / self.img['w'] * self.db.imageSize(im)[0]) * magic 
        im.lanczosScaleTransform(sf)

        # shift the image placement by the difference between where the face starts and where the spotlight is located
        im_x = self.spotlight['x'] - round(self.face['x'] / self.img['w'] * self.db.imageSize(im)[0]) # this line of code took me four hours
        im_y = self.spotlight['y'] - ( self.img['h'] - self.face['h'] - self.face['y'] ) / self.img['h'] * self.db.imageSize(im)[1] # this line of code took me two hours
        self.db.image(im, (im_x, im_y))

    def renderRetina(self):
        self.spotlight['d'] *= 2
        self.spotlight['x'] *= 2
        self.spotlight['y'] *= 2
        self.margin *= 2
        self.width *= 2
        self.height *= 2
        self.logo['x'] *= 2
        self.logo['y'] *= 2
        self.content['fontSize'] *= 2
        self.content['textBox']['width'] *= 2
        self.content['textBox']['height'] *= 2
        self.button = { 'fontSize': 12 * 2, 'width': 124 * 2, 'height': 40 * 2, 'borderRadius': 3 * 2 }

    def render(self, magic, frame_path, copy, cta):
        if len(copy) > 0:
            self.copy = copy[:self.content['character_limit']]
        else:
            self.copy = LOREM[:self.content['character_limit']]
        self.cta = cta
        self.color_scheme = 'blue'
        if (frame_path.find('_b') != -1):
            self.color_scheme = 'pink'
        self.db.newDrawing()
        self.db.size(self.width, self.height)
        self.renderPortrait(magic)
        self.renderFrame(frame_path)
        self.renderLogo()

        #randomize the order of the content of the ad
        # renderFunctions = [self.renderBadge, self.renderCopy, self.renderButton]
        # shuffle(renderFunctions)
        # cursor = self.height
        # for i in range(0,len(renderFunctions)):
        #     cursor = renderFunctions[i](cursor)

        cursor = self.renderBadge(self.height)
        cursor = self.renderCopy(cursor)
        cursor = self.renderButton(cursor)

    def save(self, fp):
        self.db.saveImage(fp)
        
    def end(self):
        self.db.endDrawing()
