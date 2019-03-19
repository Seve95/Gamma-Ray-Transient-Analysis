#!/usr/bin/env python3

import cv2 
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import sys

#arg 1: skymap file 

def maxIntensity(im, dim):
	max = 0
	for i in range(0, dim):
		for j in range(0, dim):
			if im[i][j] > max:
				max = im[i][j]
	return max

skymap = sys.argv[1]

file = fits.open(skymap)
matrix = file[0].data
wcs = WCS(file[0].header)

m = np.array(matrix, dtype='uint8')

mSmoothed = cv2.blur(m,(3,3))
m = mSmoothed

kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(m,cv2.MORPH_OPEN, kernel)

ma = maxIntensity(opening,200)

# Cancello eventuali punti di background rimasti 
# è comunque possibile avere più punti blob con massima intensità
for i in range(0, 200):
	for j in range(0,200):
		if opening[i][j] < ma:
			opening[i][j] = 0 	
		else:
			opening[i][j] = 255

params = cv2.SimpleBlobDetector_Params()
params.filterByColor = False
params.minArea = 1
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(opening)

if len(keypoints) > 0:
	# Se abbiamo più di un blob con massima intensità, seleziono quello con area 
	# maggiore e rimuovo gli altri, in caso in cui il maggiore non abbia un area 
	# maggiore di una certa soglia, allora non è considerato sorgente
	if len(keypoints) > 1:
		maxArea = 0
		indexOfMax = 0
		for i in range(0,len(keypoints)):
			if(keypoints[i].size > maxArea):
				# print(str(keypoints[i].size) + '(' + str(keypoints[i].pt[0])+ ',' +
				# 	str(keypoints[i].pt[1])+')')
				maxArea = keypoints[i].size
				indexOfMax = i
		#Thresholding 
		if maxArea > 6:
			keypoints[0] = keypoints[indexOfMax]
			while len(keypoints) > 1:
				keypoints.pop(1)
		else:
			print('Source not found')
			exit(1)

	im_with_keypoints = cv2.drawKeypoints(opening, keypoints, np.array([]), 
	(0,0,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

	ra, dec = wcs.all_pix2world(keypoints[0].pt[0], keypoints[0].pt[1], 1, ra_dec_order=True)
	print('RA: ' + str(ra))
	print('DEC: ' + str(dec))

	plt.imshow(m,cmap='gray')
	plt.show()

	plt.imshow(opening,cmap='gray')
	plt.show()

	plt.imshow(im_with_keypoints,cmap='gray')
	plt.show()
else:
	print('Source not found')