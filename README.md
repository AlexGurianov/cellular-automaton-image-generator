# Cellular Automaton Image Generator

### Overview
This script allows to create a video of the given image being generated with the cellular automaton (or just observe the process). The particular cellular automaton used in this project is [Brian's Brain](https://en.wikipedia.org/wiki/Brian's_Brain), which produces chaotic looking patterns.

The provided image is first preprocessed. Its edges are detected (using [Sobel filter](https://en.wikipedia.org/wiki/Sobel_operator)) and turned to black. Then the image is gradually drawn from scratch with the cellular automaton functioning over the image matrix. When a black pixel is hit by an alive cell of the automaton, it stays on. Generation ends when almost all black pixels in the image have been drawn.

The image generation process can be saved as an mp4 video file. The end result may be fun to look at. Then if you like, you will be able to use any converter to create a gif.

### Example
<img src="https://drive.google.com/uc?export=view&id=1U6BFHDCie46ehcsGmwyb8BUbsPqDKskG" width=49% alt="cat image"> <img src="https://www.dropbox.com/s/yqrz4kc5iq3ibm4/git_cat_gif.gif?dl=1" width=49% alt="cat gif">
<br><br> Original image and gif converted from the generated mp4 file<br>

### Requirements
This code uses Python 2.7 and the following standard libraries (all part of [Anaconda](https://www.continuum.io/downloads)):
- numpy
- matplotlib
- PIL
- skimage
- os
- copy
- argparse

They can also be installed using pip.

Additionally you will need to install either [ffmpeg](https://ffmpeg.org/) or [mencoder](http://www.mplayerhq.hu/design7/dload.html) to create and save the mp4 file.

### Usage

To start generation of the given image download and run the script from the command line with the following command. Pass the path to the image you wish to generate as a requiered `--image` argument. Add `--s` or `--save` flag to save image generation as a video file. Then wait for 'Generation finished' message.

```
python img_gen.py --image "/path/to/image" --s
```

### Parameters

To display Help with the list of all available options run

```
python img_gen.py --h
```

You can specify the following optional parameters

- --size : size of the larger side for the output image, the other side would be calculated to preserve aspect ratio. Default value is 500.
- --core : width and height of the central rectangular generating core (initial state of the automaton). Default is 100x100.
- --dying : number of iterations for the automaton cells to die out when generation is finished. Default value is 20.
- --disp : % of remaining undrawn pixels when image generation can be stopped. Default value is 0.1%.
- --s/--save : flag for saving the mp4 file. If not set, you will watch an image being generated in real time (may be a bit slow).
- --spath : path for saving the mp4 file. If not specified, video is saved to a file "animation.mp4" in the script directory.
- --fps : frames per second in the video. Each frame corresponds to one step for the automaton. Default value is 20.
