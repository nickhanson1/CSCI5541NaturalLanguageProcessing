#USAGE
#
# python3 visualize <filename>.wav
# 
# where <filename> is the name of the .wav file you wish to be visaulized
# Will visualize the frequency space of half of the recording and store the
# resulting file in <filename>_visual.png

import sys
import nltk
from scipy.io import wavfile
import numpy as np
from numpy import fft

from PIL import Image


def visualize(filename):
	size = 25 / 1000
	shift = 10 / 1000

	frequency, data = wavfile.read(filename)

	frame_count = len(data)
	window_count = int(.75 * (frame_count / frequency) / shift)

	size_slices = int(size * frequency) 
	shift_slices = int(shift * frequency)


	window_list = []

	for i in range(window_count):
		start_slice = shift_slices * i
		window = data[start_slice : start_slice + size_slices]
		window_list.append(window)


	fft_window_list = []
	max_frequency = 0

	for i in range(window_count):
		window = window_list[i]
		fft_window = fft.fft(window)
		magnitude_window = np.abs(fft_window)
		log_magnitude_window = 10 * np.log10(magnitude_window)
		fft_window_list.append(log_magnitude_window)

		max = np.amax(log_magnitude_window)
		max_frequency = max if (max > max_frequency) else max_frequency


	pix_per_time = 2
	image_name = filename[:-4] + "_visual.png"
	image = Image.new("RGB", (window_count * pix_per_time, size_slices))


	for i in range(window_count):
		window = fft_window_list[i]
		for j in range(size_slices):
			val = window[j] / max_frequency
			color = int((1 - val) * 255)

			for k in range(pix_per_time):
				image.putpixel((pix_per_time * i + k, size_slices - j - 1), (color, color, color))

	print("Saved as", image_name)
	image.save(image_name)








if len(sys.argv) < 2:
	print("Missing arguments!")
else:
	visualize(sys.argv[1])