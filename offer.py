from roundedRect import roundedRect
from random import shuffle

LOREM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

class Offer:
    def __init__(self, db, template):
        sf = 4
        self.noto = db.installFont('assets/NotoSans-Regular.ttf')
        self.recoleta = db.installFont('assets/Latinotype - Recoleta Regular.otf')
        self.recoleta_bold = db.installFont('assets/Latinotype - Recoleta Medium.otf')
        self.db = db
        self.content = template['content']
        self.content['fontSize'] *= sf
        self.content['textbox_offer']['width'] *= sf
        self.content['textbox_offer']['height'] *= sf
        self.button = { 'fontSize': 12 * sf, 'width': 100 * sf, 'height': 34 * sf, 'borderRadius': 4 * sf}
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
        copy_x = self.margin
        copy_y = cursor - (self.margin / 1.5) - self.content['textbox_offer']['height']
        self.db.textBox(self.copy, (copy_x, copy_y, self.content['textbox_offer']['width'], self.content['textbox_offer']['height']))
        cursor = copy_y 
        return cursor

    def renderOffer(self, discount):
        self.db.stroke(1)
        self.db.strokeWidth(4)
        self.db.fill(None)
        boxHeight = 140
        y_pos = self.height / 2 - boxHeight / 2
        self.db.rect(self.margin, y_pos, self.width - self.margin * 2, boxHeight)
        self.db.stroke(None)
        self.db.fill(1)
        self.db.font(self.recoleta_bold, self.content['fontSize'] * .65)
        self.db.textBox(discount, (self.margin + self.margin / 4, y_pos - boxHeight / 4, self.width - self.margin * 2, boxHeight))
        return y_pos
    
    def renderButton(self):
        self.db.blendMode('normal')
        self.switchFill('pink')
        if self.color_scheme == 'pink': 
            self.switchFill('blue')
        button_y = self.margin 
        button_x = self.width - self.margin - self.button['width']
        self.db.stroke(0,0,0,.1)
        self.db.strokeWidth(1)
        roundedRect(self.db, button_x, button_y, self.button['width'], self.button['height'], self.button['borderRadius'])
        self.db.stroke(None)
        self.db.font('Noto Sans')
        self.db.fontSize(self.button['fontSize'])
        # self.db.fontVariations(wght=3, width=2)
        self.db.fill(1) # product pink
        self.db.textBox(self.cta, (button_x, button_y - self.button['height'] / 4, self.button['width'], self.button['height']), align="center")
        # cursor -= self.button['height']
        return button_y

    def renderBadge(self):
        badge = self.db.ImageObject('assets/badge.png')
        badge_size = self.db.imageSize(badge)[0]
        sf = self.button['width'] / badge_size
        badge.lanczosScaleTransform(sf)

        badge_y = self.db.imageSize(badge)[1] + self.margin / 1.5
        badge_x = self.margin
        self.db.blendMode('normal')
        self.db.image(badge, (badge_x, badge_y))
        return badge_y

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

    def render(self, frame_path, copy, cta):
        self.copy = copy 
        # self.copy = LOREM[:self.content['character_limit']]
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
        self.renderOffer('Get 20% off any Wordpress.com plan')
        self.renderBadge()
        self.renderButton()

    def save(self, fp):
        self.db.saveImage(fp)
        
    def end(self):
        self.db.endDrawing()
