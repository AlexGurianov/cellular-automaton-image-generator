# cellular-automaton-image-generator
Generate a given image with cellular automaton

#### Overview
This script allows to create a video of the given image being generated with the cellular automaton (or just observe the process). The particular cellular automaton used in this project is [Brian's Brain](https://en.wikipedia.org/wiki/Brian's_Brain).

The provided image is first preprocessed. Its edges are detected (using [Sobel filter](https://en.wikipedia.org/wiki/Sobel_operator)) and turned to black. Then the image is gradually drawn from scratch with the cellular automaton functioning over the image matrix. When a black pixel is hit by an alive cell of the automaton, it stays on. Generation finishes when almost all black pixels in the image have been drawn.

The image generation can be saved as video to an mp4 file. The end result may be fun to look at. Then you will be able for example to create a gif with any converter.

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

They can also be installed using pip.

Additionally you will need to install either [ffmpeg](https://ffmpeg.org/) or [mencoder](http://www.mplayerhq.hu/design7/dload.html) to create and save the mp4 file.

#### Usage

To start generation of the given image run the script from the command line with the following command passing the path to the image you wish to generate as a requiered `--image` argument. Add `--s` or `--save` flag to save image generation as a video file.

```
python img_gen.py --image "/path/to/image.jpg" --s
```

#### Parameters

To display Help with all of the available options run

```
python img_gen.py --h
```

You can specify the following optional parameters

- --size - size of the larger side for the output image, the other side would be calculated to preserve aspect ratio. Default value is 500.
- --core - width and height of the central rectangular generating core (initial state of the automaton). Default is 100x100.
- --dying - number of iterations for the automaton cells to die out when generation is finished. Default value is 20.
- --disp - % of remaining undrawn pixels when image generation can be stopped. Default value is 0.1%.
- --s/--save - flag for saving the mp4 file. If not set, you will watch an image being generated in real time (may be a bit slow).
- --spath - path for saving the mp4 file. If not specified, video is saved to a file "animation.mp4" in the script directory.
- --fps - frames per second in the video. Each frame corresponds to one step for the automaton. Default value is 20.
