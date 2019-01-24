import React, {Component} from 'react';
import P5Wrapper from 'react-p5-wrapper';
import * as faceapi from 'face-api.js';

const DIMENSIONS = {
  width: 960,
  height: 540
}

const SPOTLIGHT = {
  x: DIMENSIONS.width * 0.7,
  y: DIMENSIONS.height * 0.5,
  diameter: DIMENSIONS.width * 0.375
}

export default class Sketch extends Component {
  render(){
    return (
      <P5Wrapper sketch={sketch} />
    )
  }
}

async function detectFaces(){
  const MODEL_URL = '/assets/models';
  const canvas = document.getElementById('defaultCanvas0');

  await faceapi.loadSsdMobilenetv1Model(MODEL_URL);

  const detection = await faceapi.detectSingleFace(canvas); 

  return detection
};

function drawFrame(p, frame, frameMask){
  // draw the frame
  frame = p.createImage(p.width, p.height);
  frame.loadPixels();
  for (let x = 0; x < frame.width; x++) {
    for (let y = 0; y < frame.height; y++) {
      frame.set(x, y, [36, 95, 132, 255]);
    }
  }
  frame.updatePixels();
  frame.mask(frameMask);
  p.tint(255, 225);
  p.image(frame, p.width / 2, p.height / 2);
  p.noTint();
}

function drawPortrait(p, portrait, portraitMask, relativeBox){
  p.background(255);
  p.imageMode(p.CENTER);
  portrait.resize(0, p.height);
  portrait.mask(portraitMask); // create the fade effect
  if (relativeBox !== undefined){
    console.log(relativeBox._x, relativeBox._y);
    p.image(portrait, SPOTLIGHT.x + (relativeBox._x - 0.5) * portrait.width, SPOTLIGHT.y + (relativeBox._y * portrait.height / 2));
  } else {
    p.image(portrait, SPOTLIGHT.x, SPOTLIGHT.y);
  }
}

function drawSpotlight(p){
  // draw the pink circle
  p.ellipseMode(p.CENTER);
  p.fill(229,199,212,100);
  p.noStroke();
  p.ellipse(680,270, 360, 360);
}

function sketch(p){
  let img, imgMask, frame, frameMask;

	p.preload = function() {
		img = p.loadImage('assets/removebg_2.png');
		imgMask = p.loadImage('assets/mask_reverse.png');
    frameMask = p.loadImage('assets/mask_16-9.png');
	}

	p.setup = function() {
		p.createCanvas(DIMENSIONS.width, DIMENSIONS.height);

    drawPortrait(p, img, imgMask);

    drawSpotlight(p);

    detectFaces().then((r)=>{
      // result = r.relativeBox;
      drawPortrait(p, img, imgMask, r.relativeBox);
      drawFrame(p, frame, frameMask);
      drawSpotlight(p);
    });
	}

	p.draw = function() {
    // console.log(p.mouseX + ',' + p.mouseY);
    // if (result !== undefined){
    //   p.rect(
    //     result._x * p.width, 
    //     result._y * p.height, 
    //     result._width * p.width, 
    //     result._height * p.height);
      
    //   result = undefined;
    // }
	}
}

