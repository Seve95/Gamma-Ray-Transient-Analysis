#!/usr/bin/env python3

import cv2 
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import sys
import gammalib

#arg 1: skymap file 
#arg 2: xml file

def correctCoordinates (real_ra, real_dec, ra, dec):
	if abs(real_ra - ra) < 0.1 and abs(real_dec - dec) < 0.1:
		return True
	return False


skymap = sys.argv[1]
inmodel = sys.argv[2]
test = sys.argv[3]
log = open("log.txt","a")

# Expand environment variable
inmodel = gammalib.expand_env(inmodel)

# Extract coordinates of the model 
models  = gammalib.GModels(inmodel)
try:
	origin_ra      = models[0]["RA"].value()
	origin_dec     = models[0]["DEC"].value()
	s = 1
except:
	s = 0

file = fits.open(skymap)
matrix = file[0].data
wcs = WCS(file[0].header)

m = np.array(matrix, dtype='uint8')

mSmoothed = cv2.blur(m,(3,3))
ret,thresh1 = cv2.threshold(mSmoothed,1,255,cv2.THRESH_BINARY)

kernel = np.ones((4,4),np.uint8)
# Circular Kernel 
kernel[0][0] = 0
kernel[0][3] = 0
kernel[3][0] = 0
kernel[3][3] = 0

opening = cv2.morphologyEx(thresh1,cv2.MORPH_OPEN, kernel)

params = cv2.SimpleBlobDetector_Params()
params.filterByColor = False

params.filterByInertia = False
params.filterByConvexity = False

params.filterByArea = True
params.minArea = 0

detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(opening)

isFound = False
foundOne = False

if s == 1:
	print('Origin RA: ' + str(origin_ra))
	print('Oriring DEC: ' + str(origin_dec) + ('\n'))

if len(keypoints) == 0:
	#try with lower threshold
	ret,thresh1 = cv2.threshold(mSmoothed,0,255,cv2.THRESH_BINARY)
	opening = cv2.morphologyEx(thresh1,cv2.MORPH_OPEN, kernel)
	keypoints = detector.detect(opening)

if len(keypoints) == 1:
	isFound = True
	foundOne = True
	ra, dec = wcs.all_pix2world(keypoints[0].pt[0], keypoints[0].pt[1], 1, ra_dec_order=True)
	im_with_keypoints = cv2.drawKeypoints(opening, keypoints, np.array([]), 
	(0,0,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
	print('RA: ' + str(ra))
	print('DEC: ' + str(dec))

	if s == 1:
		if correctCoordinates(origin_ra, origin_dec, ra, dec):
			#True positive
			log.write(skymap + " " + str(s) + " " + str(origin_ra) + " " + str(origin_dec) + " " + str(1) + " " +
				str(ra) + " " + str(dec) + " TP\n")

		else:
			#wrong coordinates, so a false postive
			log.write(skymap + " " + str(s) + " " + str(origin_ra) + " " + str(origin_dec) + " " + str(1) + " " +
				str(ra) + " " + str(dec) + " FP\n")
	else:
		#False positive
		log.write(skymap + " " + str(s) + " " + "-" + " " + "-" + " " + str(1) + " " +
			str(ra) + " " + str(dec) + " FP\n")

if len(keypoints) > 1:
	isFound = True

	tmp = 0
	tmpMax = 0
	tmpIndex = 0
	i = 0
	for k in keypoints:
		ra, dec = wcs.all_pix2world(k.pt[0], k.pt[1], 1, ra_dec_order=True)
		print(str(i))
		print('RA: ' + str(ra))
		print('DEC: ' + str(dec))
		print(str(k.size) + '\n')
		tmp = tmp + k.size
		if k.size > tmpMax:
			tmpMax = k.size
			tmpIndex = i
		i = i + 1

	av = tmp/len(keypoints)
	ratio = tmpMax/av

	print('\nAVARAGE: ' + str(av))
	print('MAX AREA: ' + str(tmpMax))
	print('RAPPORTO: ' + str(ratio))

	im_with_keypoints = cv2.drawKeypoints(opening, keypoints, np.array([]), 
	(0,0,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

	if ratio > 1.49:

		ra, dec = wcs.all_pix2world(keypoints[tmpIndex].pt[0], keypoints[tmpIndex].pt[1], 1, ra_dec_order=True)
		print('RA: ' + str(ra))
		print('DEC: ' + str(dec))

		if s == 1:
			if correctCoordinates(origin_ra, origin_dec, ra, dec):
				#True positive
				log.write(skymap + " " + str(s) + " " + str(origin_ra) + " " + str(origin_dec) + " " + str(1) + " " +
					str(ra) + " " + str(dec) + " TP\n")

			else:
				#wrong coordinates, so a false postive
				log.write(skymap + " " + str(s) + " " + str(origin_ra) + " " + str(origin_dec) + " " + str(1) + " " +
					str(ra) + " " + str(dec) + " FP\n")
		else:
			#False positive
			log.write(skymap + " " + str(s) + " " + "-" + " " + "-" + " " + str(1) + " " +
				str(ra) + " " + str(dec) + " FP\n")
	else:
		print('Source not found')
		if s == 1:
			#False negative
			log.write(skymap + " " + str(s) + " " + str(origin_ra) + " " + str(origin_dec) + " " + str(0) + " " +
				"-" + " " + "-" + " FN\n")
		else:
			#True negative
			log.write(skymap + " " + str(s) + " " + "-" + " " + "-" + " " + str(0) + " " +
				"-" + " " + "-" + " TN\n")

if isFound == False and foundOne == False:
	if s == 1:
		#False negative
		log.write(skymap + " " + str(s) + " " + str(origin_ra) + " " + str(origin_dec) + " " + str(0) + " " +
			"-" + " " + "-" + " FN\n")
	else:
		#True negative
		log.write(skymap + " " + str(s) + " " + "-" + " " + "-" + " " + str(0) + " " +
			"-" + " " + "-" + " TN\n")

log.close()

if test == "0":
	plt.imshow(m,cmap='gray')
	plt.show()

	plt.imshow(mSmoothed,cmap='gray')
	plt.show()

	plt.imshow(thresh1,cmap='gray')
	plt.show()

	plt.imshow(opening,cmap='gray')
	plt.show()

	if isFound:
		plt.imshow(im_with_keypoints,cmap='gray')
		plt.show()