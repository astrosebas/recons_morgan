#alias list, etc?

import os
import glob
import pandas as pd
from astropy.io import fits
from re import findall

#-matches need to be EXACT matches. some discrepancies here
#see: HIP079702, A, & B. also G2k000062 missing capital K not matching

#some epochs are not 2000... ctrl+F 2013.5
#year '19 there is a _2, correct to _B?

###do_stuff per year, for specific comments..
##creates the df for data in headers

#year 17
def do_stuff17(file):
	global datalist
	hdu = fits.open(file)
	data = hdu[0]
	filenames.append(file)
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

#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],'objectname': [data.header['OBJECT']],\
'ra_j2000': [data.header['RA']], 'dec_j2000': [data.header['DEC']],'shutter_ut_time_date':\
[data.header['UTSHUT']], 'exptime': [data.header['EXPTIME']], 'emavg': [data.header['EMAVG']], 'decker':\
[data.header['DECKER']], 'epoch': [data.header['EPOCH']], 'airmass': [data.header['airmass']],\
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
	datalist.append(df)
	return

#year 2018
def do_stuff18(file):
	global datalist
	hdu = fits.open(file)
	data = hdu[0]
	filenames.append(file)
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

#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],'objectname': [data.header['OBJECT']],\
'ra_j2000': [data.header['RA']], 'dec_j2000': [data.header['DEC']],'shutter_ut_time_date':\
[data.header['UTSHUT']], 'exptime': [data.header['EXPTIME']], 'emavg': [data.header['EMAVG']], 'decker':\
[data.header['DECKER']], 'epoch': [data.header['EPOCH']], 'airmass': [data.header['airmass']],\
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
	datalist.append(df)
	return

#year 2019
def do_stuff19(file):
	global datalist
	hdu = fits.open(file)
	data = hdu[0]
	filenames.append(file)
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

#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],'objectname': [data.header['OBJECT']],\
'ra_j2000': [data.header['RA']], 'dec_j2000': [data.header['DEC']],'shutter_ut_time_date':\
[data.header['UTSHUT']], 'exptime': [data.header['EXPTIME']], 'emavg': [data.header['EMAVG']], 'decker':\
[data.header['DECKER']], 'epoch': [data.header['EPOCH']], 'airmass': [data.header['airmass']],\
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

	datalist.append(df)
	return

#year 2020
def do_stuff20(file):
	global datalist
	hdu = fits.open(file)
	data = hdu[0]
	filenames.append(file)
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

#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],'objectname': [data.header['OBJECT']],\
'ra_j2000': [data.header['RA']], 'dec_j2000': [data.header['DEC']],'shutter_ut_time_date':\
[data.header['UTSHUT']], 'exptime': [data.header['EXPTIME']], 'emavg': [data.header['EMAVG']], 'decker':\
[data.header['DECKER']], 'epoch': [data.header['EPOCH']], 'airmass': [data.header['airmass']],\
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

	datalist.append(df)
	return

#year 2021
def do_stuff21(file):
	global datalist
	hdu = fits.open(file)
	data = hdu[0]
	filenames.append(file)
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

#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],'objectname': [data.header['OBJECT']],\
'ra_j2000': [data.header['RA']], 'dec_j2000': [data.header['DEC']],'shutter_ut_time_date':\
[data.header['UTSHUT']], 'exptime': [data.header['EXPTIME']], 'emavg': [data.header['EMAVG']], 'decker':\
[data.header['DECKER']], 'epoch': [data.header['EPOCH']], 'airmass': [data.header['airmass']],\
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

	datalist.append(df)
	return

#year 2022
def do_stuff22(file):
	global datalist
	hdu = fits.open(file)
	data = hdu[0]
	filenames.append(file)
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

#construct dataframe
	df = pd.DataFrame({'plan_id': [data.header['PROPID']],'objectname': [data.header['OBJECT']],\
'ra_j2000': [data.header['RA']], 'dec_j2000': [data.header['DEC']],'shutter_ut_time_date':\
[data.header['UTSHUT']], 'exptime': [data.header['EXPTIME']], 'emavg': [data.header['EMAVG']], 'decker':
[data.header['DECKER']], 'epoch': [data.header['EPOCH']], 'airmass': [data.header['airmass']],\
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

	datalist.append(df)
	return

#year 2023
def do_stuff23(file):
        global datalist
        hdu = fits.open(file)
        data = hdu[0]
        filenames.append(file)
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

#construct dataframe
        df = pd.DataFrame({'plan_id': [data.header['PROPID']],'objectname': [data.header['OBJECT']],\
'ra_j2000': [data.header['RA']], 'dec_j2000': [data.header['DEC']],'shutter_ut_time_date':\
[data.header['UTSHUT']], 'exptime': [data.header['EXPTIME']], 'emavg': [data.header['EMAVG']], 'decker':
[data.header['DECKER']], 'epoch': [data.header['EPOCH']], 'airmass': [data.header['airmass']],\
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

        datalist.append(df)
        return



#--------------------------------------------------------------------------------------------------------------------------------------------
#end year-by-year catalog editing

print("beginning spectra gathering")
#create lists to append later
datalist = []
filenames = []
comments = []

#load in year-by-year files to add into catalog
os.chdir('../../../morgan/chiron/tous/mir7/fitspec')
pipe_list1 = sorted(glob.glob('17*/*.fits'))
[do_stuff17(file) for file in pipe_list1]
print("completed year 2017")
pipe_list2 = sorted(glob.glob('18*/*.fits'))
[do_stuff18(file) for file in pipe_list2]
print("completed year 2018")
pipe_list3 = sorted(glob.glob('19*/*.fits'))
[do_stuff19(file) for file in pipe_list3]
print("completed year 2019")
pipe_list4 = sorted(glob.glob('20*/*.fits'))
[do_stuff20(file) for file in pipe_list4]
print("completed year 2020")
pipe_list5 = sorted(glob.glob('21*/*.fits'))
[do_stuff21(file) for file in pipe_list5]
print("completed year 2021")
pipe_list6 = sorted(glob.glob('22*/*.fits'))
[do_stuff22(file) for file in pipe_list6]
print("completed year 2022")
pipe_list7 = sorted(glob.glob('23*/*.fits'))
[do_stuff23(file) for file in pipe_list7]
print("completed year 2023")

#remove calibrations files
df = pd.concat(datalist)
df['filename'] = filenames
df['comments'] = comments #not lining up
plist = ['390', '417', '428', '464', '465', '477', '485', '489', '490', '507', '521', '522', '546', '553', '581', '643', '667', '668', '739',\
'742']
df = df[df['plan_id'].isin(plist)]
df = df[df['objectname'] != 'ThAr']
df = df[df['objectname'] != 'JUNK']

#reindex
df = df.sort_values('objectname')
df.reset_index(drop = True, inplace=True)

print("creating num_obs, main_name columns")
##num_obs, main_name
num_obs = []
main_name = []

#python magic to ignore "-1" index error
prekeyword = str(df.loc[0, 'objectname'])
prematch = str(df['objectname'].tolist())
precount = sum([len(findall(prekeyword, prematch))])
num_obs.append(precount)
main_name.append(df.loc[0, 'objectname'])

for h in range(1, precount):
	if (df.loc[h, 'objectname'] == df.loc[0, 'objectname']):
		num_obs.append(' ')
		main_name.append(' ')
	else:
		break

for i in range(precount, len(df['objectname'])):
	if (df.loc[i, 'objectname'] == df.loc[i-1, 'objectname']):
		num_obs.append(' ')
		main_name.append(' ')
	#bc for some reason having the char "+" does not work
	elif ('+' in df.loc[i, 'objectname']):
		match = df['objectname'].to_list()
		match = [k.replace('+', ';') for k in match]
		keyword = str(match[i])
		match = str(match)
		count = sum([len(findall(keyword, match))])
		num_obs.append(count)
		main_name.append(df.loc[i, 'objectname'])
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

df['num_obs'] = num_obs
df['main_name'] = main_name

printing("fixing names")
for j in range(0, len(df['objectname'])):
	if ('_A' in df.loc[j, 'main_name']):
		df.loc[j, 'main_name'] = df.loc[j, 'main_name'].replace("_A", "A")
	if ('_B' in df.loc[j, 'main_name']):
		df.loc[j, 'main_name'] = df.loc[j, 'main_name'].replace("_B", "B")
	if ('_2' in df.loc[j, 'main_name']):
		df.loc[j, 'main_name'] = df.loc[j, 'main_name'].replace("_2", "B")


#reorder columns
df = df[['main_name', 'plan_id', 'num_obs', 'objectname', 'filename', 'ra_j2000','dec_j2000', 'shutter_ut_time_date', 'exptime', 'emavg',\
 'decker', 'epoch', 'airmass', 'temp_chiron', 'comments']]

print("writing spectroscopic catalog file")

#create file
os.chdir('../../../../users/tjohns') #change this directory to yours
with open('spectroscopic-catalog_230728.txt','a') as f: 
	df_str = df.to_string(index=False, justify = 'left')
	f.write(df_str)
