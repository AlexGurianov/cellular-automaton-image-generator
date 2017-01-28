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

Additionally you will need to install either [ffmpeg](https://ffmpeg.org/) or [mencoder](http://www.mplayerhq.hu/design7/dload.html) in order to create and save the mp4 file.

#### Usage

To run generation of the given image execute the following command in the command line passing image path as a requiered argument.

```
python img_gen.py --image "/path/to/image.jpg"
```

#### Parameters

To display Help with all of the available options run

```
python img_gen.py --h
```

You can specify the following optional parameters

* --size - size of the larger side for the output image, the other side would be calculated to preserve aspect ratio. Default value is 500.
* --core - width and height of the central rectangular generating core (initial state of the automaton). Default is 100x100.
