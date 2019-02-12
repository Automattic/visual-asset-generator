from roundedRect import roundedRect

class Spotlight:
    def __init__(self, db, face, template):
        self.noto = db.installFont('/Users/jeff-ong/Library/Fonts/NotoSans-Regular.ttf')
        self.db = db
        sf = 1
        if (template['name'].find('@2x') != -1):
            sf = 2
        template['spotlight']['d'] *= sf
        template['spotlight']['x'] *= sf
        template['spotlight']['y'] *= sf
        template['dimensions']['width'] *= sf
        template['dimensions']['height'] *= sf
        template['logo']['x'] *= sf
        template['logo']['y'] *= sf

        self.button = { 'fontSize': 12 * sf, 'width': 124 * sf, 'height': 40 * sf, 'borderRadius': 3 * sf }
        self.cta = 'Start for free'
        self.resolution = sf
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
        frame_size = self.db.imageSize(frame)[0]
        sf = self.width / frame_size
        frame.lanczosScaleTransform(sf)
        # mask = self.db.ImageObject('assets/mask_{}.png'.format(self.mask))
        # frame.blendWithMask(backgroundImage=None, maskImage=mask)
        self.db.blendMode('normal')
        self.db.image(frame, (0,0), .90)

    def renderButton(self):
        self.db.fill(213/255,44/255,130/255) # product pink
        buttonMargin = self.width * .1
        if (self.height < self.width):
            buttonMargin = self.height * .1
        buttonY = self.height - buttonMargin - self.button['height']
        buttonX = buttonMargin 
        roundedRect(self.db, buttonX, buttonY, self.button['width'], self.button['height'], self.button['borderRadius'])
        self.db.font('Noto Sans Bold')
        self.db.fontSize(self.button['fontSize'])
        self.db.fill(1) # product pink
        self.db.textBox(self.cta, (buttonX, buttonY - self.button['height'] / 4, self.button['width'], self.button['height']), align="center")

    def renderPortrait(self, magic, shift):
        self.db.fill(1,1,1,1)
        self.db.rect(0,0,self.width, self.height)
        # self.spotlight['x'] = self.width * shift

        im = self.db.ImageObject(self.img['path'])
        im.photoEffectMono()
        mask = self.db.ImageObject('assets/mask_fade.png')
        # im.blendWithMask(backgroundImage=None, maskImage=mask)

        #scale the portrait to fit the spotlight
        sf = self.spotlight['d'] / (self.face['w'] / self.img['w'] * self.db.imageSize(im)[0]) * magic 
        im.lanczosScaleTransform(sf)

        # shift the image placement by the difference between where the face starts and where the spotlight is located
        im_x = self.spotlight['x'] - round(self.face['x'] / self.img['w'] * self.db.imageSize(im)[0]) # this line of code took me four hours
        im_y = self.spotlight['y'] - ( self.img['h'] - self.face['h'] - self.face['y'] ) / self.img['h'] * self.db.imageSize(im)[1] # this line of code took me two hours
        self.db.image(im, (im_x, im_y))

    def render(self, magic, shift):
        self.db.newDrawing()
        self.db.size(self.width, self.height)
        self.renderPortrait(magic, shift)
        self.renderFrame()
        self.renderLogo()
        self.renderButton()

    def save(self, fp):
        self.db.saveImage(fp)
        
    def end(self):
        self.db.endDrawing()
