import os
import argparse
import numpy as np
import matplotlib
matplotlib.use("qt4agg")

from matplotlib import rcParams
from matplotlib.cbook import is_string_like

import matplotlib.pyplot as plt
from copy import deepcopy
from PIL import Image, ExifTags
from matplotlib import animation
from skimage.color.adapt_rgb import adapt_rgb, each_channel
from skimage.exposure import rescale_intensity
from skimage.color import rgb2gray
from skimage import filters


"""input parsing"""

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def check_size(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("size %s is not positive" % value)
    elif ivalue > 1000:
        raise argparse.ArgumentTypeError("size %s is > 1000" % value)
    return ivalue


def build_parser():
    parser = argparse.ArgumentParser(prog='Image Generator')
    parser.add_argument('--image',
            dest='image', help='path to the content image',
            metavar='IMAGE', required=True)
    parser.add_argument('--size',
            dest='size',
            help='size of the larger side for the output image, <= 1000 pixels', type=check_size,
            metavar='LARGER SIDE SIZE', default=500)
    parser.add_argument('--core',
            dest='core', help='size of the central rectangular generating core',nargs=2,
            type=check_size, metavar=('CORE SIZE_X', 'CORE SIZE_Y'), default=[100, 100])
    parser.add_argument('--dying', type=check_positive,
            dest='dying', help='# of iterations for dying pixels at the end',
            metavar='DYING DURATION', default=20)
    parser.add_argument('--disp', type=check_positive,
            dest='disp', help='%% of remaining undrawn pixels when stopping',
            metavar='DISPENSABLE PIXELS', default=0.1)
    parser.add_argument('--s', '--save', action="store_true",
            dest='save', help='flag for saving the mp4 file')
    parser.add_argument('--spath',
            dest='spath', help='path for saving the mp4 file',
            metavar='SAVE PATH', default='')
    parser.add_argument('--fps', type=check_positive,
            dest='fps', help='frames per second in the video',
            metavar='FPS', default=20)
    return parser


"""making the video"""

ON = 1
DYING = 70
OFF = 255

init = [ON, DYING, OFF]

base_fig = 10.0

dying_count = 0

animation_active = True
wait_image = 0

writers = animation.writers

class newAnimation(animation.FuncAnimation):
    def save(self, filename, writer=None, fps=None, dpi=None, codec=None,
             bitrate=None, extra_args=None, metadata=None, extra_anim=None,
             savefig_kwargs=None):
        """stop saving not after an arbitrary time, but when generation is finished"""

        savefig_kwargs = {}

        if self._first_draw_id is not None:
            self._fig.canvas.mpl_disconnect(self._first_draw_id)
            reconnect_first_draw = True
        else:
            reconnect_first_draw = False

        writer = rcParams['animation.writer']

        dpi = rcParams['savefig.dpi']
        if dpi == 'figure':
            dpi = self._fig.dpi

        codec = rcParams['animation.codec']

        bitrate = rcParams['animation.bitrate']

        if is_string_like(writer):
            if writer in writers.avail:
                writer = writers[writer](fps, codec, bitrate,
                                         extra_args=extra_args,
                                         metadata=metadata)
            else:
                import warnings
                warnings.warn("MovieWriter %s unavailable" % writer)

                try:
                    writer = writers[writers.list()[0]](fps, codec, bitrate,
                                                        extra_args=extra_args,
                                                        metadata=metadata)
                except IndexError:
                    raise ValueError("Cannot save animation: no writers are "
                                     "available. Please install mencoder or "
                                     "ffmpeg to save animations.")

        with writer.saving(self._fig, filename, dpi):
            self._init_draw()
            d = 0
            while animation_active or wait_image < 5*fps:
                d += 1
                self._draw_next_frame(d, blit=False)
                writer.grab_frame(**savefig_kwargs)

        if reconnect_first_draw:
            self._first_draw_id = self._fig.canvas.mpl_connect('draw_event',
                                                               self._start)


def init_globals(size_var, center_size_var, dying_len_var, disp_pixels_var):
    global size
    global center_size
    global dying_len
    global field_old
    global field_new
    global formed_image
    global display_image
    global dying_map
    global dispensable_pixels

    size = (size_var[1], size_var[0])
    center_size = tuple(center_size_var)
    dying_len = dying_len_var

    field_old = np.ones(size, dtype=int) * 255
    field_new = np.ones(size, dtype=int) * 255
    formed_image = np.ones(size, dtype=int) * 255
    display_image = np.ones(size, dtype=int) * 255
    dying_map = np.random.randint(dying_len, size=size)

    dispensable_pixels = int(np.floor(disp_pixels_var * len(ind_pict) / 100.0))


def read_image(path):
    im = Image.open(path)
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    if im._getexif() is not None:
        exif = dict(im._getexif().items())

        if exif[orientation] == 3:
            im = im.rotate(180, expand=True)
        elif exif[orientation] == 6:
            im = im.rotate(270, expand=True)
        elif exif[orientation] == 8:
            im = im.rotate(90, expand=True)
    return im, im.size


@adapt_rgb(each_channel)
def sobel_each(image):
    return filters.sobel(image)


def process_image(image):
    """detect edges and make the image black-and-white"""
    global ind_pict

    image = rescale_intensity(1 - sobel_each(image))
    image = rgb2gray(image)

    ind_pict = []
    for i in xrange(image.shape[0]):
        for j in xrange(image.shape[1]):
            if image[i][j] < 0.9:
                ind_pict.append([i, j])


def update_cell(i, j):
    global field_new

    if field_old[i, j] == ON:
        field_new[i, j] = DYING
    elif field_old[i, j] == DYING:
        field_new[i, j] = OFF


def iter():
    """perform Brian's Brain cellular automaton step and show the updated image"""

    global field_old
    global display_image
    global ind_pict
    global dying_count
    global animation_active
    global wait_image

    if len(ind_pict) < dispensable_pixels:
        if dying_count == dying_len:
            if animation_active:
                anim.event_source.stop()
                fig.canvas.set_window_title("It's done")
                animation_active = False
            else:
                wait_image += 1
        else:
            ind = (dying_map == dying_count)
            field_new[ind] = OFF
            dying_count += 1
    else:

        for i in xrange(size[0]):
            for j in xrange(size[1]):
                update_cell(i, j)
        temp_pad = np.pad(field_old, ((1, 1), (1, 1)), 'constant')
        temp = temp_pad[2:, 1:-1] + temp_pad[:-2, 1:-1] + temp_pad[1:-1, 2:] + temp_pad[1:-1, :-2] + temp_pad[2:, 2:] + \
               temp_pad[2:,:-2] + temp_pad[:-2,2:] + temp_pad[:-2,:-2]
        ind = (temp%5 == 2*ON) & (field_old == OFF)

        field_new[ind] = ON

        field_old = deepcopy(field_new)
        for el in ind_pict:
            if ind[el[0]][el[1]]:
                formed_image[el[0]][el[1]] = ON
                ind_pict.remove(el)

        if np.min(field_new) == OFF:
            field_old[(size[0] - center_size[0]) / 2:(size[0] + center_size[0]) / 2,
            (size[1] - center_size[1]) / 2:(size[1] + center_size[1]) / 2] = np.random.randint(3, size=center_size)

            field_old[(size[0] - center_size[0]) / 2:(size[0] + center_size[0]) / 2,
            (size[1] - center_size[1]) / 2:(size[1] + center_size[1]) / 2] = \
                np.vectorize(lambda x: init[x])(field_old[(size[0] - center_size[0]) / 2:(size[0] + center_size[0]) / 2,
                                                (size[1] - center_size[1]) / 2:(size[1] + center_size[1]) / 2])

    display_image = np.minimum(formed_image, field_new)


def in_init():
    im.set_data(field_old)
    return im,


def animate(i):
    iter()
    im.set_data(display_image)
    return im,


def render_image(im_path, size_larger, center_cize_v, dying_v, disp_v, save, spath, fps):
    global dispensable_pixels
    global im
    global anim
    global fig

    image, size_real = read_image(im_path)

    if size_real[0] < size_real[1]:
        size_v = (int(np.floor(float(size_larger)*size_real[0]/size_real[1])), size_larger)
        figsize = (base_fig * size_v[0] / size_v[1], base_fig)
    else:
        size_v = (size_larger, int(np.floor(float(size_larger)*size_real[1]/size_real[0])))
        figsize = (base_fig, base_fig * size_v[1] / size_v[0])

    image = np.asarray(image.resize(size_v))
    process_image(image)

    init_globals(size_v, center_cize_v, dying_v, disp_v)

    field_old[(size[0]-center_size[0])/2:(size[0]+center_size[0])/2, (size[1]-center_size[1])/2:(size[1]+center_size[1])/2] = np.random.randint(3, size=center_size)

    field_old[(size[0]-center_size[0])/2:(size[0]+center_size[0])/2, (size[1]-center_size[1])/2:(size[1]+center_size[1])/2] = \
        np.vectorize(lambda x: init[x])(field_old[(size[0]-center_size[0])/2:(size[0]+center_size[0])/2, (size[1]-center_size[1])/2:(size[1]+center_size[1])/2])

    fig = plt.figure(frameon=False, figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    im = ax.imshow(image, cmap='hot', animated=True)
    fig.canvas.set_window_title('Building...')

    anim = newAnimation(fig, animate, init_func=in_init, interval=1, blit=True, repeat=True)

    if save or spath != '':
        if spath == '':
            spath = "animation.mp4"
            anim.save(spath, fps=fps)
            print 'Generation finished'
    else:
        plt.show()


def main():
    parser = build_parser()
    options = parser.parse_args()
    if not os.path.isfile(options.image):
        parser.error("Image %s does not exist" % options.image)
    render_image(options.image, options.size, options.core, options.dying, options.disp, options.save, options.spath, options.fps)


main()