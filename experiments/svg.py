import sys
sys.path.append('./')
sys.path.append('./../')
import drawBot as db

width = 300
height = 250
db.newDrawing()
db.size(width, height)
# db.fill(0, .9)
# db.rect(0, 0, width, height)
# db.stroke(1)
frame = db.ImageObject('assets/300_250_a@8x.png')
sf = width / frame.size()[0]
db.scale(sf)
db.image(frame, (0,0))
db.scale(1/sf)
badge = db.ImageObject('assets/badge.png')
sf = 500 / db.imageSize(badge)[0]
badge.lanczosScaleTransform(sf)
print(badge.size())
db.blendMode('difference')
db.image(badge, (30, 30))
db.saveImage('outputs/svg_test.png')
db.endDrawing()
