import numpy as np
import cv2
import drawBot

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('assets/removebg_1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 5)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    # eyes = eye_cascade.detectMultiScale(roi_gray)
    # for (ex,ey,ew,eh) in eyes:
    #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

img_h, img_w, channels = img.shape
print(img_w, img_h)

drawBot.newDrawing()
drawBot.newPage(img_w, img_h)
drawBot.fill(1)
print(x,y)
drawBot.oval(y, x, round(h*2.2), round(h*2.2)) # translate
drawBot.image("assets/removebg_1.png", (0,0))
drawBot.saveImage("outputs/db_test.png")
drawBot.endDrawing()

# cv2.imwrite('outputs/classified-{}_{}.png'.format(x,y), img)
# print(x,y,w,h)
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
