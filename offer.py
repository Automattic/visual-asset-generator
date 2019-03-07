from roundedRect import roundedRect
from random import shuffle

LOREM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

class Offer:
    def __init__(self, db, template):
        sf = 4
        self.sf = sf
        self.noto = db.installFont('assets/NotoSans-Regular.ttf')
        self.recoleta = db.installFont('assets/Latinotype - Recoleta Light.otf')
        # self.recoleta = db.installFont('assets/Latinotype - Recoleta Regular.otf')
        self.recoleta_bold = db.installFont('assets/Latinotype - Recoleta Medium.otf')
        self.db = db
        self.content = template['content']
        self.content['fontSize'] *= sf
        button = template['button']
        self.button = { 'fontSize': button['fontSize'] * sf, 'width': button['width'] * sf, 'height': button['height'] * sf, 'borderRadius': button['borderRadius'] * sf}
        self.width = template['dimensions']['width'] * sf
        self.height = template['dimensions']['height'] * sf
        self.spotlight = template['circle']
        self.spotlight['d'] *= sf
        self.spotlight['x'] *= sf
        self.spotlight['y'] *= sf
        self.logo = template['logo']
        self.logo['x'] *= sf
        self.logo['y'] *= sf
        self.db.stroke(None)
        self.db.blendMode('normal')
        self.margin = self.width * .075
        if (self.height < self.width):
            self.margin = self.height * .075

    def renderCopy(self, cursor):
        self.db.fill(1)
        self.db.blendMode('normal')
        self.db.font(self.recoleta, self.content['fontSize'])
        x = self.content['textbox_offer']['copy']['x'] * self.sf
        y = self.content['textbox_offer']['copy']['y'] * self.sf
        w = self.content['textbox_offer']['copy']['width'] * self.sf
        h = self.content['textbox_offer']['copy']['height'] * self.sf
        # copy_y = cursor - (self.margin / 1.5) - self.content['textbox_offer']['height']
        self.db.textBox(self.copy, (x, y, w, h), align=self.content['align'])

    def renderOffer(self, discount):
        self.db.stroke(1)
        self.db.strokeWidth(4)
        self.db.fill(None)
        x = self.content['textbox_offer']['box']['x'] * self.sf
        y = self.content['textbox_offer']['box']['y'] * self.sf
        w = self.content['textbox_offer']['box']['width'] * self.sf
        h = self.content['textbox_offer']['box']['height'] * self.sf
        if self.content['textbox_offer']['box']['outline'] > 0:
            self.db.rect(x, y, w, h)
        self.db.stroke(None)
        self.db.fill(1)
        self.db.font(self.recoleta_bold, self.content['textbox_offer']['box']['fontsize'] * self.sf)
        margin = h / 4
        if self.content['align'] == 'center':
            margin = 0
        self.db.textBox(discount, (x + margin, y - h / 5, w, h), align=self.content['align'])

    def renderButton(self):
        self.db.blendMode('normal')
        self.switchFill('pink')
        if self.color_scheme == 'pink': 
            self.switchFill('blue')
        x = self.content['textbox_offer']['cta']['x'] * self.sf
        y = self.content['textbox_offer']['cta']['y'] * self.sf
        self.db.stroke(0,0,0,.1)
        self.db.strokeWidth(1)
        roundedRect(self.db, x, y, self.button['width'], self.button['height'], self.button['borderRadius'])
        self.db.stroke(None)
        self.db.font('Noto Sans')
        self.db.fontSize(self.button['fontSize'])
        self.db.fill(1) # product pink
        self.db.textBox(self.cta, (x, y - self.button['height'] / 4, self.button['width'], self.button['height']), align="center")

    def renderBadge(self):
        badge = self.db.ImageObject('assets/badge.png')
        badge_size = self.db.imageSize(badge)[0]
        sf = self.content['textbox_offer']['badge']['width'] * self.sf / badge_size
        badge.lanczosScaleTransform(sf)
        # y = self.db.imageSize(badge)[1] + self.margin / 1.5
        # x = self.margin
        x = self.content['textbox_offer']['badge']['x'] * self.sf
        y = self.content['textbox_offer']['badge']['y'] * self.sf

        self.db.blendMode('normal')
        self.db.image(badge, (x, y))

    def renderLogo(self):
        logo = self.db.ImageObject('assets/logo_mark_light_gray.png')
        logo_size = self.db.imageSize(logo)[0]
        sf = self.spotlight['d'] / logo_size
        logo.lanczosScaleTransform(sf)

        self.db.blendMode('multiply')
        self.db.image(logo, (self.logo['x'], self.logo['y']))

    def switchFill(self, colorName):
        if (colorName == 'pink'):
            self.db.fill(213/255,44/255,130/255) # product pink
        elif (colorName == 'blue'):
            self.db.fill(1/255,96/255,135/255) # product blue
        else:
            self.db.fill(35/255,53/255,75/255) # product slate

    def renderFrame(self, frame_path):
        self.db.blendMode('multiply')
        self.switchFill(self.color_scheme)
        self.db.rect(0,0,self.width, self.height)
        self.db.fill(.85)
        self.db.oval(self.spotlight['x'], self.spotlight['y'], self.spotlight['d'], self.spotlight['d'])

    def render(self, frame_path, copy, cta, offer):
        self.copy = copy 
        self.offer = offer
        self.cta = 'Get started'
        if (frame_path.find('_a') > -1):
            self.color_scheme = 'pink'
        elif (frame_path.find('_b') > -1):
            self.color_scheme = 'blue'
        else:
            self.color_scheme = 'slate'
        self.db.newDrawing()
        self.db.size(self.width, self.height)
        self.renderFrame(frame_path)
        self.renderLogo()

        self.renderCopy(self.height)
        self.renderOffer(self.offer)
        self.renderBadge()
        self.renderButton()

    def save(self, fp):
        self.db.saveImage(fp)
        
    def end(self):
        self.db.endDrawing()
