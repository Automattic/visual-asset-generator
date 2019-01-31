import numpy as np
import cv2
import drawBot

DIMENSIONS = {
  'width': 1920,
  'height': 1080
}

SPOTLIGHT = {
  'x': round(DIMENSIONS['width'] * 0.6),
  'y': round(DIMENSIONS['height'] * 0.3),
  'd': round(DIMENSIONS['width'] * 0.375)
}

class Spotlight:
    def __init__(self, db, img_path, d, s):
        self.db = db
        self.width = d['width']
        self.height = d['height']
        self.spotlight = s
        self.img = { 'path': img_path, 'w': 0, 'h': 0 }
        self.face = { 'x': 0, 'y': 0, 'w': 0, 'h': 0 } 

    def classify(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        img = cv2.imread(self.img['path'])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        for f in faces:
            (x,y,w,h) = f
            if w > 300:
                break

        if w < 300:
            print('no faces found')
            sys.exit()

        self.face['x'] = x
        self.face['y'] = y
        self.face['w'] = w
        self.face['h'] = h

        img_h, img_w, channels = img.shape
        self.img['w'] = img_w
        self.img['h'] = img_h

    # def renderCopy(self):
        # drawBot.fill(1)
        # drawBot.font(RECOLETA, 88)
        # drawBot.blendMode('normal')
        # drawBot.text('Start a hat company.', (100, 350))

    def renderFrame(self):
        frame = self.db.ImageObject('assets/{}_{}.png'.format(str(int(self.width)), str(int(self.height))))
        mask = self.db.ImageObject('assets/mask_16-9.png')
        frame.blendWithMask(backgroundImage=None, maskImage=mask)
        self.db.blendMode('normal')
        self.db.image(frame, (0,0), .9)

    def renderPortrait(self, magic):
        self.db.fill(1,1,1,1)
        self.db.rect(0,0,self.width, self.height)

        im = self.db.ImageObject(self.img['path'])
        im.photoEffectMono()

        #scale the portrait to fit the spotlight
        print(self.face)
        print(self.img)
        print(self.db.imageSize(im))
        sf = self.spotlight['d'] / (self.face['w'] / self.img['w'] * self.db.imageSize(im)[0]) * magic 
        print(sf)
        im.lanczosScaleTransform(sf)
        print(self.db.imageSize(im))

        # shift the image placement by the difference between where the face starts and where the spotlight is located
        im_x = self.spotlight['x'] - round(self.face['x'] / self.img['w'] * self.db.imageSize(im)[0]) # this line of code took me four hours
        im_y = self.spotlight['y'] - ( self.img['h'] - self.face['h'] - self.face['y'] ) / self.img['h'] * self.db.imageSize(im)[1] # this line of code took me two hours
        print(im_x, im_y)
        self.db.image(im, (im_x, im_y))
        self.db.oval(self.spotlight['x'], self.spotlight['y'], 10, 10)

    def render(self, magic):
        self.db.newDrawing()
        self.db.size(self.width, self.height)
        self.renderPortrait(magic)
        self.renderFrame()

    def save(self, fp):
        self.db.saveImage(fp)
        
    def end(self):
        self.db.endDrawing()

if __name__ == "__main__":
    RECOLETA = drawBot.installFont('/Users/jeff-ong/Library/Fonts/Latinotype - Recoleta Regular.otf')
    # ad = Spotlight(drawBot, 'assets/GettyImages-915095050.jpg', DIMENSIONS, SPOTLIGHT) # silver fox 
    # ad = Spotlight(drawBot, 'assets/GettyImages-1020581962.jpg', DIMENSIONS, SPOTLIGHT) # josh musick
    # ad = Spotlight(drawBot, 'assets/GettyImages-908040972.jpg', DIMENSIONS, SPOTLIGHT) # glasses woman
    ad = Spotlight(drawBot, 'assets/GettyImages-1012208544.jpg', DIMENSIONS, SPOTLIGHT) # glasses woman
    ad.classify()
    magic_numbers = [1, 4/5, 3/5, 2/3, 1/2]
    for magic_number in magic_numbers:
        ad.render(magic_number)
        ad.save("outputs/scale_test_{}.png".format(magic_number))
    ad.end()


#OPENCV
    # eyes = eye_cascade.detectMultiScale(roi_gray)
    # for (ex,ey,ew,eh) in eyes:
    #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
