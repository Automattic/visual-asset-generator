# Visual Asset Generator

A python application for generating Wordpress.com brand assets. 

## Getting Started

### Installation
In the project's root directory, [compile drawbot as a python module](https://github.com/typemytype/drawbot).

After compiling drawbot, install the remaining requirements. It's recommended to run this application using a python virtual environment. From your terminal: 

`virtualenv env`

`source env/bin/activate`

`pip install -r requirements.txt`

The project depends on [drawBot](https://drawbot.com) and [python resize image](https://github.com/charlesthk/python-resize-image).

### Usage

```Bash
./local.sh
```

OR 

Invoke the python application directly:

```Bash
python app.py [options]
```

#### Options

##### --format

Currently supports: 
- `300_250` (70 character limit)
- `300_600` (105 character limit)
- `160_600` (140 character limit)
- `970_250` (140 character limit)

###### --copy 

The copy that should populate the asset. The character limit depends on the format.

###### --cta 

The copy that should populate the button.

### Packaging for Distribution

1. Generate a setup file:

  `py2applet --make-setup app.py`

2. Edit `setup.py` to include the assets (images) and data (templates and faces) directories:

`DATA_FILES = ['data', 'assets']`

3. Remove existing dist and build directories:

`rm -rf dist build`

4. Build app:

`python setup.py py2app`

### Instructions for installing OpenCV

OpenCV is used to determine the position of faces in a batch of portraits. To use opencv for python:

- Install python bindings for OpenCV (here are [instructions](https://medium.com/@nuwanprabhath/installing-opencv-in-macos-high-sierra-for-python-3-89c79f0a246a) for MacOS)
- Link haar-cascade pre-trained classifier, e.g.:
    `$ ln -s /usr/local/opt/opencv/share/opencv4/haarcascades/haarcascade_frontalface_default.xml haarcascade_frontalface_default.xml`
    
## What's Not Included

Portraits and other assets used in composing the images.

## What's Next
- There has active discussions around its usage in international markets, however automated translation is often imperfect. Adding the ability to export layers that can be pulled into image compositing software (e.g. Sketch, Figma) is an alternative to allow for global content managers to edit.
- Further automating this process to generate assets seeded with audience and market specific demographics.
