#!/usr/bin/env python3
import gammalib
import ctools
import cscripts
import sys
import random
import os
import model

#arg 1: number of events
#arg 2: destination folder 

path = os.getcwd()
folder = sys.argv[2]

os.mkdir(folder)
os.chdir(folder)

n = int(sys.argv[1])
init_ra  = 83.63
init_dec = 22.51

for x in range(0,n):
	sim = ctools.ctobssim()
	smap = ctools.ctskymap()
	newModel = 'sigma4(' + str(x) + ').xml'
	ra = round(init_ra + random.uniform(-1,1),5)
	dec = round(init_dec + random.uniform(-1,1),5)
	model.createNewModel(path + '/sigma4.xml', newModel, ra, dec)
	
	sim['inmodel'] = newModel
	sim['outevents'] = 'events' + str(x) +'.fits'
	sim['caldb']     = 'prod2'
	sim['irf']       = 'South_0.5h'
	sim['ra']        = init_ra
	sim['dec']       = init_dec
	sim['rad']       = 5.0
	sim['tmin']      = '2020-01-01T00:00:00'
	sim['tmax']      = '2020-01-01T01:00:00'
	sim['emin']      = 0.1
	sim['emax']      = 100.0
	sim.execute()
	
	print('[' + str(int(((x + 1)/ n)*100)) + '%] - Generated' + ' events' + str(x) +'.fits -> (RA: ' + str(ra) + ', DEC: ' + str(dec) + ')')

	smap['inobs']       = 'events' + str(x) +'.fits'
	smap['outmap']      = 'skymap' + str(x) + '.fits'
	smap['emin']        = 0.1
	smap['emax']        = 100.0
	smap['bkgsubtract'] = 'NONE'
	smap['coordsys']    = 'CEL'
	smap['xref']        = init_ra
	smap['yref']        = init_dec
	smap['proj']        = 'CAR'
	smap['binsz']       = 0.02
	smap['nxpix']       = 200
	smap['nypix']       = 200
	smap.execute()

print('---DONE---')
