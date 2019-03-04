import sys
sys.path.append('./')
sys.path.append('./../')
import drawBot as db
from random import shuffle
from os import listdir
from os.path import isfile, join

width = 970
height = 600

files = [f for f in listdir('outputs/gif/') if isfile(join('outputs/gif', f))]
shuffle(files)

db.newDrawing()
db.size(width, height)
for i in range(len(files)):
    fp = 'outputs/gif/'+files[i]
    print(fp)
    db.newPage(width, height)
    db.frameDuration(.25)
    # db.fill(0)
    # db.rect(0,0,width,height)
    # db.fill(None)
    im = db.ImageObject(fp)
    if (im.size()[1] == height):
        pos = ((width -im.size()[0]) / 2, 0)
    elif (im.size()[0] == width):
        pos = (0, (height - im.size()[1]) / 2)
    else:
        pos = ( (width - im.size()[0]) / 2, (height - im.size()[1]) / 2 )

    db.image(im, pos)
db.saveImage('outputs/gif_slow.gif')
db.endDrawing()
