#!/usr/bin/env python3

import cv2 
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import sys
import gammalib
import os

#arg 1: number fo map to test

tot = int(sys.argv[1])
found = False

for i in range(0,tot):
	for file in os.listdir("."):
		currentMap = "skymap" + str(i) + ".fits"
		if file == currentMap:
			currentModel = "sigma4-" + str(i) + ".xml"
			os.system("python sourceCoordinates.py " + currentMap + " " + currentModel + " 1")
			found = True
			break
	
	if found == False:
		currentMap = "skymapNS" + str(i) + ".fits"
		currentModel = 'noSource.xml'
		os.system("python sourceCoordinates.py " + currentMap + " " + currentModel + " 1")