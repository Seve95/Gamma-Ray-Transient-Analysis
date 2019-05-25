#!/usr/bin/env python3

import cv2 
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import sys
import gammalib
import os
import io

def inc(value):
	global tp
	global tn
	global fp
	global fn

	if value == "TP":
		tp =  tp + 1
	if value == "TN":
		tn = tn + 1
	if value == "FP":
		fp = fp + 1
	if value == "FN":
		fn = fn + 1

#arg 1: number fo map to test
#arg 2: 1 = mapWithSource, otherwise without source

tot = int(sys.argv[1])
source = int(sys.argv[2])
found = False

for i in range(0,tot):
	if source == 1:
		currentMap = "skymap" + str(i) + ".fits"
		currentModel = "sigma4-" + str(i) + ".xml"
		os.system("python sourceCoordinates.py " + currentMap + " " + currentModel + " 1")

	else:
		currentMap = "skymapNS" + str(i) + ".fits"
		currentModel = 'noSource.xml'
		os.system("python sourceCoordinates.py " + currentMap + " " + currentModel + " 1")
	print("TESTED: " + str(i+1))

#analyze log 
log = open('log.txt',"r")

tp = 0 
tn = 0 
fp = 0
fn = 0 

results =  log.readlines()

for r in results:
	 values = r.split(' ', 8)
	 inc(values[7].replace('\n',''))

print("TP: " + str(tp))
print("FP: " + str(fp))
print("TN: " + str(tn))
print("FN: " + str(fn))