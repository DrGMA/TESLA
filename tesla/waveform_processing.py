# encoding: utf8
#!/usr/bin/env python

"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- glob
- numpy
- obspy
- rich
- shutil
- tesla.spectra_processing 
- tesla.curve_fitting 
- tesla.plot_spectra 
- tesla.save_object 
- tesla.load_object 
- tesla.spectra_selection 
"""
import glob
from obspy import read
from tesla.spectra_processing import SpectraProcessing
from tesla.curve_fitting import SpectraFitting
from tesla.plot_spectra import PlotSpectraLoop
from tesla.save_object import SaveObject
from tesla.load_object import LoadObject
from tesla.spectra_selection import SpectraSelection
import numpy as np
import shutil
from rich.console import Console
from rich.theme import Theme




def WaveformProcessing(cfg,sta,phase,console):
	"""
	Process the waveform data for a given station and seismic phase.

	Args:
	    cfg (dict): Configuration parameters.
	    sta (str): The name of the seismic station.
	    phase (str): The seismic phase to process (P or S).
	    console (bool): Flag to print progress messages to the console.

	Returns:
	    SpectraList (list): List of Spectra objects with fitted parameters and updated data.
	    Wvfrms (list): List of waveform data objects.
	    console (bool): Console flag.
	"""


	#phase=cfg["SourceSpectra"]["Phase"]
	ext=cfg["Files"]["ext"]
	min_len=cfg["WaveformProcessing"]["MinLength"]
	min_dur_sig=cfg["WaveformProcessing"]["MinDurSig"]
	max_len=cfg["WaveformProcessing"]["MaxLength"]
	wind_shift=cfg["WaveformProcessing"]["WindShift"]




	#for sta in cfg["Files"]["stations"]:

	#-----------------------------------------------------------------------------#
	#Check if waveforms of station exist. Otherwise let's skip the station 
	if len(glob.glob('*.'+sta+'.*'+'.'+ext)) == 0:  
		console.log("[warning]WARNING:[/warning]  [normal]No waveforms for station %s" %(sta))
		return [],[],console
	#-----------------------------------------------------------------------------#
	st=read('*.'+sta+'.*'+'.'+ext, debug_headers=True)
	#-----------------------------------------------------------------------------#
	#Check if waveforms have the same no. of points (or the same length). 
	#Otherwise let's skip the station 
	npts_=[]
	for k in range(3):
		npts_.append(st[k].stats.npts)

	if any(x != npts_[0] for x in npts_):
		console.log("[warning]WARNING:[/warning]  [normal]Waforms have different lengths for station %s" %(sta))
		return [],[],console
	#-----------------------------------------------------------------------------#
	for k in range(3):
		if not st[k].stats.sac.a == -12345.0:
			st[0].stats.sac.a=st[k].stats.sac.a
			st[1].stats.sac.a=st[k].stats.sac.a
			st[2].stats.sac.a=st[k].stats.sac.a
			break
	for k in range(3):
		if not st[k].stats.sac.t0 == -12345.0:
			st[0].stats.sac.t0=st[k].stats.sac.t0
			st[1].stats.sac.t0=st[k].stats.sac.t0
			st[2].stats.sac.t0=st[k].stats.sac.t0
			break
	#Check if P-pick exists. Otherwise let's skip the station
	if phase=='P':
		if st[0].stats.sac.a==-12345.0: #or st[0].stats.sac.t0==-12345.0 :
			console.log("[warning]WARNING:[/warning]  [normal]There are no P arrival times for station %s" %(sta))
			return [],[],console
	else:
		if st[0].stats.sac.a==-12345.0: #or st[0].stats.sac.t0==-12345.0 :
			console.log("[warning]WARNING:[/warning]  [normal]There are no P arrival times for station %s" %(sta))
			return [],[],console
		if st[0].stats.sac.t0==-12345.0:
			console.log("[warning]WARNING:[/warning]  [normal]There are no S arrival times for station %s" %(sta))
			return [],[],console
	#-----------------------------------------------------------------------------#
	#print(st)
	st.detrend(type='demean')
	st.detrend(type='linear')
	st.filter("bandpass",freqmin=cfg["WaveformProcessing"]["fmin"],freqmax=cfg["WaveformProcessing"]["fmax"],corners=2,zerophase=True)

	#-----------------------------------------------------------------------------#

	if phase=='P':
		P=st[0].stats.sac.a
		if not st[0].stats.sac.t0==-12345.0:
			S=st[0].stats.sac.t0
		else:
			console.log("[warning]WARNING:[/warning]  [normal]There are no S arrival times for station %s" %(sta))
			console.log("[warning]WARNING:[/warning]  [normal]Check any potential window overlap with S phase for station %s" %(sta))
			S=P+min_len+max_len
	else:
		S=st[0].stats.sac.t0 
		P0=st[0].stats.sac.a+.3
		P=st[0].stats.sac.a
	#-----------------------------------------------------------------------------#
	#min_len=0.2
	#min_dur_sig=0.2

	wind_index=0

	PSpectra=[]
	SSpectra=[]
	SpectraList=[]

	for i in np.arange(0, max_len, wind_shift):

		for j in np.arange(min_len, min_len+max_len, wind_shift):

			wind_index += 1
			#print('	')
			#print(P,S,j+i,(P-i-(j+i)))
			# print(P,P-i,P1)
			# print(i+j)

	#-----------------------------------------------------------------------------#

			if phase=='P':

				if not (P+j) < S or (j+i) < min_dur_sig or (P-i-(j+i)) < 0:

					#console.log("[warning]WARNING:[/warning]		[normal]The Signal Window No. %s is oversize!" %(wind_index))

					continue

				else:

					id="%02d.%s.%s" % (wind_index,phase,'Spctr')

					a=SpectraProcessing(cfg,id,st,i,j,sta,phase)


					b=SpectraFitting(cfg,a,phase)


					SpectraList.append(b)

	#-----------------------------------------------------------------------------#


			if phase=='S':

				if not (S-i) > P0 or (i+j) < min_dur_sig or (P-i-(j+i)) < 0:

					#console.log("[warning]WARNING:[/warning]		[normal]The Signal Window No. %s is oversize!" %(wind_index))


					continue

				else:
					
					id="%02d.%s.%s" % (wind_index,phase,'Spctr')

					c=SpectraProcessing(cfg,id,st,i,j,sta,phase)


					d=SpectraFitting(cfg,c,phase)


					SpectraList.append(d)

	Wvfrms=st


	return SpectraList, Wvfrms, console		
