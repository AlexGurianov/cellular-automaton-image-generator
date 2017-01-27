# cellular-automaton-image-generator
Generate a given image with cellular automaton

#### Overview
This script allows to create a video of the given image being generated with the cellular automaton (or just observe the process). The particular cellular automaton used in this project is [Brian's Brain](https://en.wikipedia.org/wiki/Brian's_Brain).

The provided image is first preprocessed. Its edges are detected and turned to black. Then the image is gradually drawn from scratch with the cellular automaton functioning over the image matrix. When a black pixel is hit by an alive cell of the automaton, it stays on. Generation finishes when almost all black pixels in the image have been drawn.

The process of the image generation can be saved to an mp4 file. The end result looks pretty nice. The video can be then converted for example to create a gif.

#### Example


#### Requirements
This code uses Python 2.7 and relies on the following standard libraries (all part of [Anaconda](https://www.continuum.io/downloads)):
- numpy
- matplotlib
- PIL
- skimage
- os
- copy
- argparse

They can also be installed with pip.

Additionally in order to create and save the mp4 file you will need to install either ffmpeg or .

#### Usage

To run... specify... The parameters --image must be specified

#### Parameters

To display Help run

```
python img_gen.py --h
```

You can specify the following optional parameters
