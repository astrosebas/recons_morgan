#alias list, etc?

import os
import sys
import glob
import pandas as pd
import numpy as np
from astropy.io import fits
from re import findall


from utilities.terminal_log import (log,
                                degree_to_dms,
                                degree_to_hms,
                                degree_to_mas,
                                )

from utilities.config import config_data
from science.snr_funtions import (SNREM_value,
                                  SNREM_fits
								)
								  

#-matches need to be EXACT matches. some discrepancies here
#see: HIP079702, A, & B. also G2k000062 missing capital K not matching

#some epochs are not 2000... ctrl+F 2013.5
#year '19 there is a _2, correct to _B?

###do_stuff per year, for specific comments..
##creates the df for data in headers

#year 17
def do_stuff17(file):
	
	global datalist
	global path_file
	global comments

	hdu = fits.open(file)
	data = hdu[0]
	path_file.append(file)

	#checking for missing data
	if 'RA' not in data.header:
		data.header['RA'] = '00:00:00.00'
	if 'DEC' not in data.header:
		data.header['DEC'] = '00:00:00.0'
	if 'EPOCH' not in data.header:
		data.header['epoch'] = '0.0'
	if 'airmass' not in data.header:
		data.header['airmass'] = '0.0'
	if 'EMAVG' not in data.header:
		data.header['emavg'] = '0.0'
	if 'EMNUMSMP' not in data.header:
		data.header['emnumsmp'] = '0.0'

	#special cases
	if '2MA0201+0117A' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117A'  
	if '2MA0201+0117B' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117B' 


	#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],
			            'objectname': [data.header['OBJECT']],
						'ra_j2000': [data.header['RA']],
						'dec_j2000': [data.header['DEC']],
						'epoch': [data.header['EPOCH']], 
						'shutter_ut_time_date':[data.header['UTSHUT']], 
						'exptime': [data.header['EXPTIME']],
					    'emavg': [data.header['EMAVG']],
					    'emnumsmp': [data.header['EMNUMSMP']],
						'decker': [data.header['DECKER']],
						'airmass': [data.header['airmass']],
						'temp_chiron': [data.header['TEMPTCEN']]})

	comment = ""
	#comments
	for g in range(0, len(df['objectname'])):
		if ('airmass' in df.loc[g, 'airmass']):
			df.loc[g, 'airmass'] = '0.0'
		if (df.loc[g, 'airmass'] == ''):
			df.loc[g, 'airmass'] = '0.0'
		if ('--' in df.loc[g, 'objectname']):
			objname, sep, comment = df.loc[g, 'objectname'].partition("--")
			objname = objname.strip()
			comment = comment.strip()
			df.loc[g, 'objectname'] = objname
#			comments.append(comment)
		#there's a dash that also has high airmass?
		elif('-' in df.loc[g, 'objectname']):
			objname, sep, comment = df.loc[g, 'objectname'].partition('-')
			objname = objname.strip()
			comment = comment.strip()
			df.loc[g, 'objectname'] = objname
#			comments.append(comment)
		#pesky comment separated by only a space...tsk tsk
		elif(' guiding' in df.loc[g, 'objectname']):
			objname, sep, comment = df.loc[g,'objectname'].partition(' ')
			objname = objname.strip()
			comment = comment.strip()
			df.loc[g, 'objectname'] = objname
		elif (float(df.loc[g, 'airmass']) >= 2):
			comment = comment + "high airmass"
#			comments.append("high airmass")
		if ('HIP079878-' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HIP079878'
		else:
			comment = comment + ""
	comments.append(comment)
	#datalist.append(df)

	plan = data.header['PROPID']
	obj = data.header['OBJECT']

	if plan != "Calib":
	#ob_name = hdu['OBJECT']        
		if obj not in calib:
			log.info(f'Reading {file}')
			log.info(f'Plan {plan}: {obj} read')

	datalist.append(df)
	return

#year 2018
def do_stuff18(file):

	global datalist
	global path_file
	global comments

	hdu = fits.open(file)
	data = hdu[0]
	path_file.append(file)

	#check for missing data
	if 'RA' not in data.header:
		data.header['RA'] = '00:00:00.00'
	if 'DEC' not in data.header:
		data.header['DEC'] = '00:00:00.0'
	if 'EPOCH' not in data.header:
		data.header['epoch'] = '0.0'
	if 'airmass' not in data.header:
		data.header['airmass'] = '0.0'
	if 'EMAVG' not in data.header:
		data.header['emavg'] = '0.0'
	if 'EMNUMSMP' not in data.header:
		data.header['emnumsmp'] = '0.0'

	#special cases
	if '2MA0201+0117A' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117A'  
	if '2MA0201+0117B' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117B' 


	#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],
					'objectname': [data.header['OBJECT']],\
					'ra_j2000': [data.header['RA']],\
					'dec_j2000': [data.header['DEC']],\
					'epoch': [data.header['EPOCH']], \
					'shutter_ut_time_date':[data.header['UTSHUT']], 
					'exptime': [data.header['EXPTIME']], \
					'emavg': [data.header['EMAVG']], \
					'emnumsmp': [data.header['EMNUMSMP']], \
					'decker': [data.header['DECKER']], \
					'airmass': [data.header['airmass']],\
					'temp_chiron': [data.header['TEMPTCEN']]})

#check for blank data
	for g in range(0, len(df['objectname'])):
		if ('ra' in df.loc[g, 'ra_j2000']):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if ('dec' in df.loc[g, 'dec_j2000']):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		if ('airmass' in df.loc[g, 'airmass']):
			df.loc[g, 'airmass'] = '0.0'
		if (df.loc[g, 'airmass'] == ''):
			df.loc[g, 'airmass'] = '0.0'
		#special cases, do I need to do these on A & B separate observations?
		if (df.loc[g, 'objectname'] == 'HIP06336'):
			df.loc[g, 'objectname'] = 'HIP063366'
		if (df.loc[g, 'objectname'] == 'HIO054418'):
			df.loc[g, 'objectname'] = 'HIP054418'
		if (df.loc[g, 'objectname'] == 'G2k000062'):
			df.loc[g, 'objectname'] = 'G2K000062'
		if (df.loc[g, 'objectname'] == 'HIP26175'):
			df.loc[g, 'objectname'] = 'HIP026175'
		if (df.loc[g, 'objectname'] == 'HIP34341'):
			df.loc[g, 'objectname'] = 'HIP034341'
		if ('HD ' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = df.loc[g, 'objectname'].strip()
		if (float(df.loc[g, 'airmass']) >= 2):
			comments.append("high airmass")
		else:
			comments.append("")

	plan = data.header['PROPID']
	obj = data.header['OBJECT']

	if plan != "Calib":
	#ob_name = hdu['OBJECT']        
		if obj not in calib:
			log.info(f'Reading {file}')
			log.info(f'Plan {plan}: {obj} read')

	datalist.append(df)
	return

#year 2019
def do_stuff19(file):
	
	global datalist
	global path_file
	global comments

	hdu = fits.open(file)
	data = hdu[0]
	path_file.append(file)

	#check for missing data

	if 'RA' not in data.header:
		data.header['RA'] = '00:00:00.00'
	if 'DEC' not in data.header:
		data.header['DEC'] = '00:00:00.0'
	if 'EPOCH' not in data.header:
		data.header['epoch'] = '0.0'
	if 'airmass' not in data.header:
		data.header['airmass'] = '0.0'
	if 'EMAVG' not in data.header:
		data.header['emavg'] = '0.0'
	if 'EMNUMSMP' not in data.header:
		data.header['emnumsmp'] = '0.0'

	#special cases
	if '2MA0201+0117A' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117A'  
	if '2MA0201+0117B' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117B' 

	#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],
			            'objectname': [data.header['OBJECT']],
						'ra_j2000': [data.header['RA']],
						'dec_j2000': [data.header['DEC']],
						'epoch': [data.header['EPOCH']], 
						'shutter_ut_time_date':[data.header['UTSHUT']], 
						'exptime': [data.header['EXPTIME']],
					    'emavg': [data.header['EMAVG']],
					    'emnumsmp': [data.header['EMNUMSMP']],
						'decker': [data.header['DECKER']],
						'airmass': [data.header['airmass']],
						'temp_chiron': [data.header['TEMPTCEN']]})


	#check for blank data
	for g in range(0, len(df['objectname'])):
		comment = ""
		if ('--' in df.loc[g, 'objectname']):
			objname, sep, comment = df.loc[g, 'objectname'].partition("--")
			objname = objname.strip()
			comment = comment.strip()
			df.loc[g, 'objectname'] = objname
		if ('ra' in df.loc[g, 'ra_j2000']):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if ('dec' in df.loc[g, 'dec_j2000']):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		if ('airmass' in df.loc[g, 'airmass']):
			df.loc[g, 'airmass'] = '0.0'
		if (df.loc[g, 'ra_j2000'] == ''):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if (df.loc[g, 'dec_j2000'] == ''):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		#special case
		if ('HD_042074' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HD042074'
		if ('HIP 042074' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HIP042074'
		if ('HD_168442' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HD168442'
		if ('HD_221503' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HD221503'
		if ('HD_24916' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HD24916'
		if (df.loc[g, 'objectname'] == 'HIP32270'):
			df.loc[g, 'objectname'] = 'HIP032270'
		if (df.loc[g, 'objectname'] == 'HIP34034'):
			df.loc[g, 'objectname'] = 'HIP034034'
		if (df.loc[g, 'objectname'] == 'HIP35631'):
			df.loc[g, 'objectname'] = 'HIP035631'
		if (df.loc[g, 'objectname'] == 'HIP38702'):
			df.loc[g, 'objectname'] = 'HIP038702'
		if (df.loc[g, 'objectname'] == 'HIP80440'):
			df.loc[g, 'objectname'] = 'HIP080440'
		if ('HD ' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = df.loc[g, 'objectname'].strip()
		if (df.loc[g, 'airmass'] == ''):
			df.loc[g, 'airmass'] = '0.0'
		if (float(df.loc[g, 'airmass']) >= 2):
			comment = comment + " " + "high airmass"
			comments.append(comment)
		else:
			comments.append(comment)
			
	plan = data.header['PROPID']
	obj = data.header['OBJECT']
		
	if plan != "Calib":
		#ob_name = hdu['OBJECT']        
		if obj not in calib:
			log.info(f'Reading {file}')
			log.info(f'Plan {plan}: {obj} read')

	datalist.append(df)

	return

#year 2020
def do_stuff20(file):

	global datalist
	global path_file
	global comments

	hdu = fits.open(file)
	data = hdu[0]
	path_file.append(file)

	#check for missing data
	if 'RA' not in data.header:
		data.header['RA'] = '00:00:00.00'
	if 'DEC' not in data.header:
		data.header['DEC'] = '00:00:00.0'
	if 'EPOCH' not in data.header:
		data.header['epoch'] = '0.0'
	if 'airmass' not in data.header:
		data.header['airmass'] = '0.0'
	if 'EMAVG' not in data.header:
		data.header['emavg'] = '0.0'
	if 'EMNUMSMP' not in data.header:
		data.header['emnumsmp'] = '0.0'

	#special cases
	if '2MA0201+0117A' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117A'  
	if '2MA0201+0117B' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117B' 

	#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],
			            'objectname': [data.header['OBJECT']],
						'ra_j2000': [data.header['RA']],
						'dec_j2000': [data.header['DEC']],
						'epoch': [data.header['EPOCH']], 
						'shutter_ut_time_date':[data.header['UTSHUT']], 
						'exptime': [data.header['EXPTIME']],
					    'emavg': [data.header['EMAVG']],
					    'emnumsmp': [data.header['EMNUMSMP']],
						'decker': [data.header['DECKER']],
						'airmass': [data.header['airmass']],
						'temp_chiron': [data.header['TEMPTCEN']]})

	#check for blank data
	for g in range(0, len(df['objectname'])):
		comment = ""
		if ('--' in df.loc[g, 'objectname']):
			objname, sep, comment = df.loc[g, 'objectname'].partition("--")
			objname = objname.strip()
			comment = comment.strip()
			df.loc[g, 'objectname'] = objname
		if ('ra' in df.loc[g, 'ra_j2000']):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if ('dec' in df.loc[g, 'dec_j2000']):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		if ('airmass' in df.loc[g, 'airmass']):
			df.loc[g, 'airmass'] = '0.0'
		if (df.loc[g, 'ra_j2000'] == ''):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if (df.loc[g, 'dec_j2000'] == ''):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		if ('HD ' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = df.loc[g, 'objectname'].strip()
		if (df.loc[g, 'airmass'] == ''):
			df.loc[g, 'airmass'] = '0.0'
		if (float(df.loc[g, 'airmass']) >= 2):
			comment = comment + " " + "high airmass"
			comments.append(comment)
		else:
			comments.append(comment)

	plan = data.header['PROPID']
	obj = data.header['OBJECT']
		
	if plan != "Calib":
		#ob_name = hdu['OBJECT']        
		if obj not in calib:
			log.info(f'Reading {file}')
			log.info(f'Plan {plan}: {obj} read')

	datalist.append(df)
	return

#year 2021
def do_stuff21(file):

	global datalist
	global path_file
	global comments

	hdu = fits.open(file)
	data = hdu[0]
	path_file.append(file)
	

	#check for missing data
	if 'RA' not in data.header:
		data.header['RA'] = '00:00:00.00'
	if 'DEC' not in data.header:
		data.header['DEC'] = '00:00:00.0'
	if 'EPOCH' not in data.header:
		data.header['epoch'] = '0.0'
	if 'airmass' not in data.header:
		data.header['airmass'] = '0.0'
	if 'EMAVG' not in data.header:
		data.header['emavg'] = '0.0'
	if 'EMNUMSMP' not in data.header:
		data.header['emnumsmp'] = '0.0'

	#special cases
	if '2MA0201+0117A' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117A'  
	if '2MA0201+0117B' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117B' 

	#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],
		    'objectname': [data.header['OBJECT']],
			'ra_j2000': [data.header['RA']], 
			'dec_j2000': [data.header['DEC']],
			'shutter_ut_time_date':[data.header['UTSHUT']], 
			'exptime': [data.header['EXPTIME']], 
			'emavg': [data.header['EMAVG']], 
			'emnumsmp': [data.header['EMNUMSMP']],
			'decker':[data.header['DECKER']], 
			'epoch': [data.header['EPOCH']], 
			'airmass': [data.header['airmass']],
			'temp_chiron': [data.header['TEMPTCEN']]})

#check for blank data
	for g in range(0, len(df['objectname'])):
		comment = ""
		if ('--' in df.loc[g, 'objectname']):
			objname, sep, comment = df.loc[g, 'objectname'].partition("--")
			objname = objname.strip()
			comment = comment.strip()
			df.loc[g, 'objectname'] = objname
		if ('ra' in df.loc[g, 'ra_j2000']):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if ('dec' in df.loc[g, 'dec_j2000']):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		if ('airmass' in df.loc[g, 'airmass']):
			df.loc[g, 'airmass'] = '0.0'
		if (df.loc[g, 'ra_j2000'] == ''):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if (df.loc[g, 'dec_j2000'] == ''):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		#special cases
		if ('G2K000950 A component (N)' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'G2K000950_A'
		if ('G2K000950 B component (S)' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'G2K000950_B'
		if ('G2K001172 faint companion' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'G2K001172_B'
			comment = comment + "faint companion"
		if ('G2K001325 brighter NE' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'G2K001325'
			comment = comment + "brighter NE"
		if ('G2K001325 fainter SW' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'G2K001325'
			comment = comment + "fainter SW"
		if ('HIP058345 cloudy' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HIP058345'
			comment = comment + "cloudy"
		if ('HIP079878 cloudy, moved' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HIP079878'
			comment = comment + "cloudy, moved"
		if (df.loc[g, 'airmass'] == ''):
			df.loc[g, 'airmass'] = '0.0'
		if (float(df.loc[g, 'airmass']) >= 2):
			comment = comment + " " + "high airmass"
			comments.append(comment)
		else:
			comments.append(comment)

	plan = data.header['PROPID']
	obj = data.header['OBJECT']
		
	if plan != "Calib":
		#ob_name = hdu['OBJECT']        
		if obj not in calib:
			log.info(f'Reading {file}')
			log.info(f'Plan {plan}: {obj} read')

	#print('emnumsmp',df['emnumsmp'])	
		
	datalist.append(df)
	return

#year 2022
def do_stuff22(file):

	global datalist
	global path_file
	global comments

	hdu = fits.open(file)
	data = hdu[0]
	path_file.append(file)

	#check for missing data
	if 'RA' not in data.header:
		data.header['RA'] = '00:00:00.00'
	if 'DEC' not in data.header:
		data.header['DEC'] = '00:00:00.0'
	if 'EPOCH' not in data.header:
		data.header['epoch'] = '0.0'
	if 'airmass' not in data.header:
		data.header['airmass'] = '0.0'
	if 'EMAVG' not in data.header:
		data.header['emavg'] = '0.0'
	if 'EMNUMSMP' not in data.header:
		data.header['emnumsmp'] = '0.0'


	#special cases
	if '2MA0201+0117A' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117A'  
	if '2MA0201+0117B' == str(data.header['OBJECT']):
		data.header['OBJECT'] = '2MA0201_0117B' 

	#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],
		    'objectname': [data.header['OBJECT']],
			'ra_j2000': [data.header['RA']], 
			'dec_j2000': [data.header['DEC']],
			'shutter_ut_time_date':[data.header['UTSHUT']], 
			'exptime': [data.header['EXPTIME']], 
			'emavg': [data.header['EMAVG']], 
			'emnumsmp': [data.header['EMNUMSMP']],
			'decker':[data.header['DECKER']], 
			'epoch': [data.header['EPOCH']], 
			'airmass': [data.header['airmass']],
			'temp_chiron': [data.header['TEMPTCEN']]})

	#check for blank data
	for g in range(0, len(df['objectname'])):
		comment = ""
		if ('--' in df.loc[g, 'objectname']):
			objname, sep, comment = df.loc[g, 'objectname'].partition("--")
			objname = objname.strip()
			comment = comment.strip()
			df.loc[g, 'objectname'] = objname
		if ('ra' in df.loc[g, 'ra_j2000']):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if ('dec' in df.loc[g, 'dec_j2000']):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
		if ('airmass' in df.loc[g, 'airmass']):
			df.loc[g, 'airmass'] = '0.0'
		if (df.loc[g, 'ra_j2000'] == ''):
			df.loc[g, 'ra_j2000'] = '00:00:00.00'
		if (df.loc[g, 'dec_j2000'] == ''):
			df.loc[g, 'dec_j2000'] = '00:00:00.0'
                #special case
		if ('HD_042074' in df.loc[g, 'objectname']):
			df.loc[g, 'objectname'] = 'HD042074'
		if (df.loc[g, 'airmass'] == ''):
			df.loc[g, 'airmass'] = '0.0'
		if (float(df.loc[g, 'airmass']) >= 2):
			comment = comment + " " + "high airmass"
			comments.append(comment)
		else:
			comments.append(comment)

	plan = data.header['PROPID']
	obj = data.header['OBJECT']
		
	if plan != "Calib":
		#ob_name = hdu['OBJECT']        
		if obj not in calib:
			log.info(f'Reading {file}')
			log.info(f'Plan {plan}: {obj} read')

	datalist.append(df)

	return

#year 2023
def do_stuff23(file):

        global datalist
        global path_file
        global comments
	
        hdu = fits.open(file)
        data = hdu[0]
		#fits_info = fits.open(path)
		#hdu = fits_info['PRIMARY'].header
		
        path_file.append(file)
	
		#check for missing data

        if 'RA' not in data.header:
                data.header['RA'] = '00:00:00.00'
        if 'DEC' not in data.header:
                data.header['DEC'] = '00:00:00.0'
        if 'EPOCH' not in data.header:
                data.header['epoch'] = '0.0'
        if 'airmass' not in data.header:
                data.header['airmass'] = '0.0'
        if 'EMAVG' not in data.header:
                data.header['emavg'] = '0.0'
        if 'EMNUMSMP' not in data.header:
                data.header['emnumsmp'] = '0.0'

		#special cases
        if '2MA0201+0117A' == str(data.header['OBJECT']):
                data.header['OBJECT'] = '2MA0201_0117A'  
        if '2MA0201+0117B' == str(data.header['OBJECT']):
                data.header['OBJECT'] = '2MA0201_0117B' 

		#construct dataframe
        df = pd.DataFrame({'plan_id': [data.header['PROPID']],
			            'objectname': [data.header['OBJECT']],\
						'ra_j2000': [data.header['RA']],\
						'dec_j2000': [data.header['DEC']],\
						'epoch': [data.header['EPOCH']], \
						'shutter_ut_time_date':[data.header['UTSHUT']], 
						'exptime': [data.header['EXPTIME']], \
					    'emavg': [data.header['EMAVG']], \
					    'emnumsmp': [data.header['EMNUMSMP']],
						'decker': [data.header['DECKER']], \
						'airmass': [data.header['airmass']],\
						'temp_chiron': [data.header['TEMPTCEN']]})
	
		#check for blank data
        for g in range(0, len(df['objectname'])):
                comment = ""
                if ('--' in df.loc[g, 'objectname']):
                        objname, sep, comment = df.loc[g, 'objectname'].partition("--")
                        objname = objname.strip()
                        comment = comment.strip()
                        df.loc[g, 'objectname'] = objname
                if ('ra' in df.loc[g, 'ra_j2000']):
                        df.loc[g, 'ra_j2000'] = '00:00:00.00'
                if ('dec' in df.loc[g, 'dec_j2000']):
                        df.loc[g, 'dec_j2000'] = '00:00:00.0'
                if ('airmass' in df.loc[g, 'airmass']):
                        df.loc[g, 'airmass'] = '0.0'
                if (df.loc[g, 'ra_j2000'] == ''):
                        df.loc[g, 'ra_j2000'] = '00:00:00.00'
                if (df.loc[g, 'dec_j2000'] == ''):
                        df.loc[g, 'dec_j2000'] = '00:00:00.0'
                #special case
          #      if ('HD_042074' in df.loc[g, 'objectname']):
          #              df.loc[g, 'objectname'] = 'HD042074'
                if (df.loc[g, 'airmass'] == ''):
                        df.loc[g, 'airmass'] = '0.0'
                if (float(df.loc[g, 'airmass']) >= 2):
                        comment = comment + " " + "high airmass"
                        comments.append(comment)
                else:
                        comments.append(comment)
		
        plan = data.header['PROPID']
        obj = data.header['OBJECT']
		
        if plan != "Calib":
			#ob_name = hdu['OBJECT']        
            if obj not in calib:
                log.info(f'Reading {file}')
                log.info(f'Plan {plan}: {obj} read')
			
        datalist.append(df)
		
        return



#--------------------------------------------------------------------------------------------------------------------------------------------
#end year-by-year catalog editing

datalist = []
path_file = []
comments = []

calib = ['ThAr','quartz','iodine']

def sb():
	print(" ▔▔▔▔▔╲")
	print("▕╮╭┻┻╮╭┻┻╮╭▕╮╲")
	print("▕╯┃╭╮┃┃╭╮┃╰▕╯╭▏")
	print("▕╭┻┻┻┛┗┻┻┛ ▕ ╰▏")
	print("▕╰━━━┓┈┈┈╭╮▕╭╮▏")
	print(" ╭╮╰┳┳┳┳╯╰╯▕╰╯▏")
	print("▕╰╯┈┗┛┗┛┈╭╮▕╮┈▏")

def rks_catalog(spec_root,outname):

	sb()
	log.info(f'BEGINNING SPECTRA GATHERING')
	
	#create lists to append later
	"""
	datasets = [dI for dI in os.listdir(spec_root) if \
                os.path.isdir(os.path.join(spec_root,dI))]
	datasets.sort()
	datasets.remove('fifteen_twenty_pc')
	datasets.remove('ten_fifteen_pc')
	datasets.remove('ten_test')
	datasets.remove('test')
	datasets.remove('twenty_five_pc')
	log.info('Datasets retrieved')
	"""
	#load in year-by-year files to add into catalog
	#os.chdir('../../../morgan/chiron/tous/mir7/fitspec')
	
	pipe_list1 = sorted(glob.glob(spec_root+'/17*/*.fits'))
	#[do_stuff17(file) for file in pipe_list1]
	for file in pipe_list1:
		do_stuff17(file)
	log.info(f'============ Year 2017 COMPLETED ============')
	sb()
		
	pipe_list2 = sorted(glob.glob(spec_root+'/18*/*.fits'))
	#[do_stuff18(file) for file in pipe_list2]
	for file in pipe_list2:
		do_stuff18(file)
	log.info(f'============ Year 2018 COMPLETED ============')
	sb()
	
	pipe_list3 = sorted(glob.glob(spec_root+'/19*/*.fits'))
	#[do_stuff19(file) for file in pipe_list3]
	for file in pipe_list3:
		do_stuff19(file)
	log.info(f'============ Year 2019 COMPLETED ============')
	sb()
	
	pipe_list4 = sorted(glob.glob(spec_root+'/20*/*.fits'))
	#[do_stuff20(file) for file in pipe_list4]
	for file in pipe_list4:
		do_stuff20(file)
	log.info(f'============ Year 2020 COMPLETED ============')
	sb()
	
	pipe_list5 = sorted(glob.glob(spec_root+'/21*/*.fits'))
	#[do_stuff21(file) for file in pipe_list5]
	for file in pipe_list5:
		do_stuff21(file)
	log.info(f'============ Year 2021 COMPLETED ============')
	sb()
	
	pipe_list6 = sorted(glob.glob(spec_root+'/22*/*.fits'))
	#[do_stuff22(file) for file in pipe_list6]
	for file in pipe_list6:
		do_stuff21(file)
	log.info(f'============ Year 2022 COMPLETED ============')
	sb()
	
	pipe_list7 = sorted(glob.glob(spec_root+'/23*/*.fits'))
	#[do_stuff23(file) for file in pipe_list7]
	for file in pipe_list7:
		do_stuff23(file)
	log.info(f'============ Year 2023 COMPLETED ============')
	

	#remove calibrations files
	df = pd.concat(datalist)
	df['pathfile'] = path_file
	df['comments'] = comments #not lining up
	plist = ['390', '417', '428', '453','464', '465', '477', '485', '489', '490', \
		'507', '521', '522', '546', '553', '581', '643', '667', '668', '734', '739','742', '747','811','818','820']
	#plist = ['734']

	df = df[df['plan_id'].isin(plist)]
	df = df[df['objectname'] != 'ThAr']
	df = df[df['objectname'] != 'JUNK']

	#reindex
	df = df.sort_values('objectname')
	df.reset_index(drop = True, inplace=True)
	#print(df.to_string())

	#for i in df['objectname']:
		#m = df['objectname'].str.startswith('2MA')
		#f.loc[m,'ISIN']='Cash'
	#	if i.str.startswith('2MA'):	
	#		match = i.to_list()
	#		match = [k.replace('+', ';') for k in match]
	#		keyword = str(match[i])
	#		match = str(match)
	#		print(keyword,match)


	#bc for some reason having the char "+" does not work
	#if ('+' in df.loc[i, 'objectname']):
		
		#match = df['objectname'].to_list()
		#match = [k.replace('+', ';') for k in match]
		#keyword = str(match[i])
		#match = str(match)
		#count = sum([len(findall(keyword, match))])
		#num_obs.append(count)
		#main_name.append(df.loc[i, 'objectname'])

	log.info(f'============ creating num_obs, main_name columns ============')
	##num_obs, main_name
	num_obs = []
	main_name = []

	#python magic to ignore "-1" index error
	prekeyword = str(df.loc[0, 'objectname'])
	prematch = str(df['objectname'].tolist())
	precount = sum([len(findall(prekeyword, prematch))])
	num_obs.append(precount)
	main_name.append(df.loc[0, 'objectname'])

	print('prekeyword',prekeyword)
	print('prematch',prematch)
	print(len(findall(prekeyword, prematch)))
	print('precount',precount)

	for h in range(1, precount):
		if (df.loc[h, 'objectname'] == df.loc[0, 'objectname']):
			num_obs.append(' ')
			main_name.append(' ')
			#print('h',h)
		else:
			#print('broke')
			break

	for i in range(precount, len(df['objectname'])):
		if (df.loc[i, 'objectname'] == df.loc[i-1, 'objectname']):
			#print(df.loc[i, 'objectname'] , df.loc[i-1, 'objectname'])
			print(f"{df.loc[i, 'objectname']} observed more than once")
			num_obs.append(' ')
			main_name.append(' ')

		#"""
		#bc for some reason having the char "+" does not work
		elif ('+' in df.loc[i, 'objectname']):
			match = df['objectname'].to_list()
			match = [k.replace('+', ';') for k in match]
			keyword = str(match[i])
			match = str(match)
			count = sum([len(findall(keyword, match))])
			num_obs.append(count)
			main_name.append(df.loc[i, 'objectname'])
		#"""

		else:
			keyword = str(df.loc[i, 'objectname'])
			count = sum([len(findall(keyword, prematch))])
			num_obs.append(count)
			main_name.append(df.loc[i, 'objectname'])
		
	#for naming consistency, A's & B's should all be attached to the star name
	for j in range(0, len(df['objectname'])):
		if ('_A' in df.loc[j, 'objectname']):
			df.loc[j, 'objectname'] = df.loc[j, 'objectname'].replace("_A", "A")
		if ('_B' in df.loc[j, 'objectname']):
			df.loc[j, 'objectname'] = df.loc[j, 'objectname'].replace("_B", "B")
		if ('_2' in df.loc[j, 'objectname']):
			df.loc[j, 'objectname'] = df.loc[j, 'objectname'].replace("_2", "B")

	#num_obs.insert(0, 0)
	df['num_obs'] = num_obs
	df['main_name'] = main_name

	for j in range(0, len(df['objectname'])):
		if ('_A' in df.loc[j, 'main_name']):
			df.loc[j, 'main_name'] = df.loc[j, 'main_name'].replace("_A", "A")
		if ('_B' in df.loc[j, 'main_name']):
			df.loc[j, 'main_name'] = df.loc[j, 'main_name'].replace("_B", "B")
		if ('_2' in df.loc[j, 'main_name']):
			df.loc[j, 'main_name'] = df.loc[j, 'main_name'].replace("_2", "B")
	log.info(f'============ fixing names ============')

	# Calculating SN for all the spectrum
	# from Paredes et al. 2021

	df['snrem'] = SNREM_value(df['emavg'], df['emnumsmp'])

	# REORDERING COLUMNS
	#df = df[['main_name', 'plan_id', 'num_obs', 'objectname', 'path', \
	#        'ra_j2000','dec_j2000', 'shutter_ut_time_date', 'exptime', 'emavg',\
	#        'decker', 'epoch', 'airmass', 'temp_chiron', 'comments']]
	
	df_final = df[['main_name', 'plan_id', 'num_obs', 'objectname',\
	        'ra_j2000','dec_j2000', 'epoch', 'airmass',\
			'shutter_ut_time_date', 'exptime', 'emavg', 'emnumsmp', 'snrem',\
			'decker', 'temp_chiron', 'pathfile', 'comments']]

	#print(df.keys())

	

	#os.chdir('../../../../users/crrzgax/Documents/recons/recons_morgan') #change this directory to yours
	#with open('spectroscopic-catalog_2308002.txt','a') as f:

	# CREATIN OUTPUT FILES

	file_txt = outname+'.txt'
	file_csv = outname+'.csv'

	with open(file_txt,'a') as f: 
		df_str = df_final.to_string(index=False, justify = 'left')
		f.write(df_str)

	df_final.to_csv(file_csv,index=False)

	log.info(f'====== PRINTING SPECTROSCOPIC CATALOG FILE ======')
