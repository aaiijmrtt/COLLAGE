import cv2, numpy as np

usage = '\n\nNAME\n\n\n\tcollage - stitch little images into larger images\n\n\nSYNOPSIS\n\n\n\t./collage.py [OPTIONS]... <IMAGEFILE>\n\n\nDESCRIPTION\n\n\n\tMake a collage. Tile together smaller images algorithmically designed to form a larger image.\n\n\tMandatory arguments to long options are mandatory for short options too.\n\n\n\t-h, --help\n\t\tdisplay this help and exit\n\n\t-v, --video[FALSE]\n\t\tinput and output are video files\n\n\t-s, --sources=FILE[IMAGEFILE]\n\t\taccept file containing paths to tiled images\n\n\t-t, --times=INT[50]\n\t\taccept granularity of collage\n\n\t-o, --output=FILE[output]\n\t\taccept name of output file\n\n\n\tIMAGEFILE\n\t\taccept the image file for the collage\n\n\nAUTHOR\n\n\n\tWritten by Amitrajit Sarkar.\n\n\nREPORTING BUGS\n\n\n\tReport bugs to <aaiijmrtt@gmail.com>.\n\n\nCOPYRIGHT\n\n\nThe MIT License (MIT)\n\nCopyright (c) 2016 Amitrajit Sarkar\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n'

def blackwhite(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def shrink(image, step):
	return image[::step, ::step]

def shift(image, bias):
	return cv2.convertScaleAbs(image, beta = bias)

def snip(image, step):
	vstep, hstep = image.shape[0] / step, image.shape[1] / step
	return [[image[i * vstep: (i + 1) * vstep,  ii * hstep: (ii + 1) * hstep] for ii in xrange(step)] for i in xrange(step)]

def mean(images, step):
	return [[np.mean(images[i][ii]) for ii in xrange(step)] for i in xrange(step)]

def recolour(images, sources, destinations, step):
	return [[shift(images[i][ii], destinations[i][ii] - sources[i][ii]) for ii in xrange(step)] for i in xrange(step)]

def stitch(images, step):
	return np.vstack([np.hstack(images[i]) for i in xrange(step)])

def collage(sources, destination, step):
	sources = [[blackwhite(shrink(sources[(i * step + ii) % len(sources)], step)) for ii in xrange(step)] for i in xrange(step)]
	patches = snip(blackwhite(destination), step)
	return stitch(recolour(sources, mean(sources, step), mean(patches, step), step), step)
