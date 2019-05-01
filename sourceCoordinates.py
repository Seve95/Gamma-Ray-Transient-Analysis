#!/usr/bin/env python3

import cv2 
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import sys

#arg 1: skymap file 

skymap = sys.argv[1]

file = fits.open(skymap)
matrix = file[0].data
wcs = WCS(file[0].header)

m = np.array(matrix, dtype='uint8')

mSmoothed = cv2.blur(m,(3,3))
ret,thresh1 = cv2.threshold(mSmoothed,2,255,cv2.THRESH_BINARY)

kernel = np.ones((5,5),np.uint8)
# Circular Kernel 
kernel[0][0] = 0
kernel[0][4] = 0
kernel[4][0] = 0
kernel[4][4] = 0

opening = cv2.morphologyEx(thresh1,cv2.MORPH_OPEN, kernel)

params = cv2.SimpleBlobDetector_Params()
params.filterByColor = False
params.minArea = 1
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(opening)

if len(keypoints) > 0:
	im_with_keypoints = cv2.drawKeypoints(opening, keypoints, np.array([]), 
	(0,0,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

	ra, dec = wcs.all_pix2world(keypoints[0].pt[0], keypoints[0].pt[1], 1, ra_dec_order=True)
	print('RA: ' + str(ra))
	print('DEC: ' + str(dec))

	plt.imshow(mSmoothed,cmap='gray')
	plt.show()

	plt.imshow(thresh1,cmap='gray')
	plt.show()

	plt.imshow(opening,cmap='gray')
	plt.show()

	plt.imshow(im_with_keypoints,cmap='gray')
	plt.show()
else:
	plt.imshow(mSmoothed,cmap='gray')
	plt.show()

	plt.imshow(thresh1,cmap='gray')
	plt.show()

	plt.imshow(opening,cmap='gray')
	plt.show()

	print('Source not found')