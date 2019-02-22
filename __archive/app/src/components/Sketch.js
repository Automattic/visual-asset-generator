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
  p.image(frame, 0, 0);
  p.noTint();
}


function drawPortrait(p, portrait, portraitMask, r){
  p.background(255);
  p.imageMode(p.CORNER);
  // portrait.mask(portraitMask); // create the fade effect

  if (r !== undefined){
    portrait.resize(0, p.height);
    const scalar = SPOTLIGHT.diameter / r.box._width;
    portrait.resize(portrait.width * scalar, 0);

    console.log(r.relativeBox);

    let shift = (r.relativeBox._x + r.relativeBox._width) * portrait.width;
    let portrait_x = SPOTLIGHT.x - shift;
    p.image(portrait, portrait_x, SPOTLIGHT.y - (r.relativeBox._height * portrait.height));

    // shift = (1 - r.relativeBox._x) * portrait.width;
    // portrait_x = SPOTLIGHT.x - shift;
    // p.image(portrait, portrait_x, SPOTLIGHT.y - (r.relativeBox._height * portrait.height));
    // p.image(portrait, 0, 0);
  } else {
    // Set height of the portrait to the height of the canvas
    portrait.resize(0, p.height);
    p.image(portrait, 0, 0);
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
		// img = p.loadImage('assets/GettyImages-97559100.jpg');
		// img = p.loadImage('assets/removebg_2.png');
		// img = p.loadImage('assets/GettyImages-908040972.jpg');
		// img = p.loadImage('assets/GettyImages-915095050.jpg');
		img = p.loadImage('assets/GettyImages-1012208544.jpg');
		imgMask = p.loadImage('assets/mask_reverse.png');
    frameMask = p.loadImage('assets/mask_16-9.png');
	}

	p.setup = function() {
		p.createCanvas(DIMENSIONS.width, DIMENSIONS.height);

    drawPortrait(p, img, imgMask);

    // drawSpotlight(p);

    const scaleFactors = [2, 1.5, 1, 0.75, .5];
    // const horizontalShift = [ -0.5, 0, 0.5 ];

    detectFaces().then((r)=>{
      drawPortrait(p, img, imgMask, r);
      drawFrame(p, frame, frameMask);
      // p.save(`shift.png`);

      // for (let i = 0; i < scaleFactors.length; i++){
      //     drawPortrait(p, img, imgMask, r, scaleFactors[i]);
      //     drawFrame(p, frame, frameMask);
      //     // drawSpotlight(p);
      //     p.save(`${i}.png`);
      // }
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

