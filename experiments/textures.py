import sys
sys.path.append('./')
import drawBot

drawBot.newDrawing()
drawBot.size(1080,1080)
im = drawBot.ImageObject('assets/1080_1080.png')
texture = drawBot.ImageObject('assets/chalkboard_invert.png')
texture.lanczosScaleTransform(2.5)
im.blendWithMask(backgroundImage=None, maskImage=texture)
mask = drawBot.ImageObject('assets/mask_square.png')
im.blendWithMask(backgroundImage=None, maskImage=mask)
drawBot.image(im, (0,0))
drawBot.saveImage('outputs/experiments/texture.png')
