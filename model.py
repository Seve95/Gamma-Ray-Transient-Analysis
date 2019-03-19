#!/usr/bin/env python3
import xml.etree.ElementTree as et
import random

def createNewModel(oldFile, newFile, ra, dec):
	tree = et.parse(oldFile)
	root = tree.getroot()
	source = root.find('source')
	sm = source.find('spatialModel')
	for p in sm.findall('parameter'):
		if p.attrib['name'] == 'RA':
			p.attrib['value'] = str(ra)
		if p.attrib['name'] == 'DEC':
			p.attrib['value'] = str(dec)

	tree.write(newFile)