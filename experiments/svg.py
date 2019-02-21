import sys
sys.path.append('./')
sys.path.append('./../')
import drawBot as db

width = 600
height = 500
db.newDrawing()
db.size(width, height)
# db.fill(0, .9)
# db.rect(0, 0, width, height)
# db.stroke(1)
frame = db.ImageObject('assets/300_250_a@8x.png')
db.image(frame, (0,0))
badge = db.ImageObject('assets/badge.png')
print(badge.size())
sf = 1000 / db.imageSize(badge)[0]
badge.lanczosScaleTransform(sf)
db.blendMode('normal')
db.image(badge, (30, 30))
db.saveImage('outputs/svg_test.png')
db.endDrawing()
