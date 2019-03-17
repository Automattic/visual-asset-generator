import cv2
import json
from os import listdir
from os.path import isfile, join

def classify(path, classifier):
    img = cv2.imread(path)
    print(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        return False

    for f in faces:
        print(f)
        (x,y,w,h) = f
        # if w > 300:
        #     break

    face = {}
    face['x'] = int(x)
    face['y'] = int(y)
    face['w'] = int(w)
    face['h'] = int(h)

    img_h, img_w, channels = img.shape
    img = {}
    img['w'] = int(img_w)
    img['h'] = int(img_h)
    data = { 'path': path, 'face': face, 'img': img }
    return data

if __name__ == "__main__":
    files = [f for f in listdir('assets/dotcom_spotlight') if isfile(join('assets/dotcom_spotlight', f))]
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = []
    for f in files:
        if '.png' in f:
            found_face = classify('assets/dotcom_spotlight/{}'.format(f), face_cascade)
            if found_face:
                faces.append(found_face)

    with open('data/dotcom_faces.json', 'w') as fp:
        fp.write(json.dumps(faces))
