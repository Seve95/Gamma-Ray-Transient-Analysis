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

for i in range(0,tot):
	currentMap = "skymap" + str(i) + ".fits"
	currentModel = "sigma4-" + str(i) + ".xml"
	os.system("python sourceCoordinates.py " + currentMap + " " + currentModel + " 1")
