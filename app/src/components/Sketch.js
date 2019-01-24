import React, {Component} from 'react';
import P5Wrapper from 'react-p5-wrapper';
import * as faceapi from 'face-api.js';

export default class Sketch extends Component {
  render(){
    return (
      <P5Wrapper sketch={sketch} />
    )
  }
}

async function detectFaces(){
  const canvas = document.getElementById('defaultCanvas0');
  await faceapi.loadSsdMobilenetv1Model('/models');
  // const detections = await faceapi.detectSingleFace(canvas); 
  // console.log(detections);
};

function sketch(p){
  let img, imgMask, frame, frameMask;

	p.preload = function() {
		img = p.loadImage('assets/removebg_3.png');
		imgMask = p.loadImage('assets/mask_reverse.png');
    frameMask = p.loadImage('assets/mask_16-9.png');
	}


	p.setup = function() {
		p.createCanvas(960, 540);
		// img.mask(imgMask);
    img.resize(0, p.height);
		frame = p.createImage(p.width, p.height);
		frame.loadPixels();
		for (let x = 0; x < frame.width; x++) {
			for (let y = 0; y < frame.height; y++) {
				frame.set(x, y, [36, 95, 132, 255]);
			}
		}
		frame.updatePixels();
    frame.mask(frameMask);

		p.imageMode(p.CENTER);
		p.background(255);
		p.image(img, p.width - img.width, p.height / 2);
    // p.tint(255, 225);
    // p.image(frame, p.width / 2, p.height / 2);


    setTimeout(detectFaces, 3000);
	}

	p.draw = function() {
    // p.rect(0,0,p.width, p.height);
	}

}
