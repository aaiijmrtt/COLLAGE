import sys, getopt
import cv2
import util

def image(sources, destination, step, compress, output):
	cv2.imwrite('%s.jpg' %output, util.collage(sources, destination, step, compress))

def video(sources, destination, step, compress, output):
	count, total = 0, destination.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
	while True:
		if not destination.grab(): break
		_source, _destination = list(), destination.retrieve()[1]
		for i in xrange(len(sources)):
			if not sources[i].grab(): break
			_source.append(sources[i].retrieve()[1])
		else:
			cv2.imwrite('%s-%05d.jpg' %(output, count), util.collage(_source, _destination, step, compress))
			if count % 10 == 0:
				sys.stdout.write('\r[%s>%s] %d%%' % ('=' * int(count / total * 20), ' ' * int((1 - count / total) * 20), int(count / total * 100)))
				sys.stdout.flush()
			count += 1
			continue
		break

def arguments(string):
	try:
		opts, args = getopt.getopt(string, 'hvs:t:c:o:', ['help', 'video', 'sources=', 'times=', 'compress=', 'output='])
		if len(args) != 1: raise Exception()
		sources, destination, compress, step, isvideo, output = [args[0]], args[0], 1, 50, False, 'output'
		for opt, arg in opts:
			if opt in ('-h', '--help'): raise Exception()
			elif opt in ('-v', '--video'): isvideo = True
			elif opt in ('-s', '--sources'): sources = [line.strip() for line in open(arg)]
			elif opt in ('-c', '--compress'): compress = int(arg)
			elif opt in ('-t', '--times'): step = int(arg)
			elif opt in ('-o', '--output'): output = arg
	except Exception as error:
		print >> sys.stderr, util.usage
		sys.exit()
	return sources, destination, step, compress, isvideo, output

if __name__ == '__main__':
	sources, destination, step, compress, isvideo, output = arguments(sys.argv[1: ])
	if not isvideo:
		sources = [cv2.imread(source) for source in sources]
		destination = cv2.imread(destination)
		image(sources, destination, step, compress, output)
	else:
		sources = [cv2.VideoCapture(source) for source in sources]
		destination = cv2.VideoCapture(destination)
		video(sources, destination, step, compress, output)
	 	for i in xrange(len(sources)): sources[i].release()
		destination.release()
