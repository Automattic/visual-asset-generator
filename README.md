# Spotlight Generator

### Instructions to get OpenCV running

- Install python bindings for OpenCV (here are [instructions](https://medium.com/@nuwanprabhath/installing-opencv-in-macos-high-sierra-for-python-3-89c79f0a246a) for MacOS)

- Link haar-cascade pre-trained classifier:
    `$ ln -s /usr/local/opt/opencv/share/opencv4/haarcascades/haarcascade_frontalface_default.xml haarcascade_frontalface_default.xml`


### Background research

https://stackoverflow.com/questions/401847/circle-rectangle-collision-detection-intersection

### Drawbot Installation

`pip3 install -U defcon`

`pip3 install -U PyObjC`

### Packaging for Distribution

1. Generate a setup file:

  `py2applet --make-setup app.py`

2. Edit `setup.py` to include the assets (images) and data (templates and faces) directories:

`DATA_FILES = ['data', 'assets']`

3. Remove existing dist and build directories:

`rm -rf dist build`

4. Build app:

`python setup.py py2app`
