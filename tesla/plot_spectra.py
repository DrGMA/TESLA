# encoding: utf8
#!/usr/bin/env python

"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- matplotlib
- numpy
- rich
- time
"""

from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
from time import process_time
from rich.console import Console



def PlotSpectraLoop(SpectraList,wvfrms,cfg,sta,phase,console,show_figure=False,save_figure=False):
	"""
	Plot and visualize the spectra for a list of Spectra objects.

	Args:
	    SpectraList (list): List of Spectra objects with fitted parameters and updated data.
	    wvfrms (list): List of waveform data objects.
	    cfg (dict): Configuration parameters.
	    sta (str): The name of the seismic station.
	    phase (str): The seismic phase to process (P or S).
	    show_figure (bool, optional): Flag to display the figure. Defaults to False.
	    save_figure (bool, optional): Flag to save the figure. Defaults to False.
	"""
	
	t1_start = process_time() 

	#phase=cfg["SourceSpectra"]["Phase"]
	show_figure=cfg["PlotFigure"]["ShowFigure"]
	save_figure=cfg["PlotFigure"]["SaveFigure"]

	first_spectra_plot= True

	for Spectra in SpectraList:


		t1_sig=Spectra.SigWindTimes[0]
		t2_sig=Spectra.SigWindTimes[1]
		t1_noise=Spectra.NoiseWindTimes[0]
		t2_noise=Spectra.NoiseWindTimes[1]

		if phase=='P':

			Pick=Spectra.Ppick
		
		else:

			Pick=Spectra.Spick

		st=wvfrms

		f1_noise=Spectra.NoiseFrequencies
		omg1_noise=Spectra.NoiseSpectrum

		f1=Spectra.SigFrequencies
		omg1=Spectra.SigSpectrum

		pred1=Spectra.CalculatedSpectrum


		#win_dur=t2-t1

		win_dur=float(Spectra.SigWindTimes[1]-Spectra.SigWindTimes[0])
		len_sig_prePick=float(Pick-Spectra.SigWindTimes[0])
		len_sig_afterPick=float(Spectra.SigWindTimes[1]-Pick)
		omega0=float(Spectra.CurveFit['Omega0'])
		corn_frq=float(Spectra.CurveFit['Fc'])
		q_val=float(Spectra.CurveFit['Q'])
		#sta=(str(Spectra.station))
		rms_fit=float(Spectra.CurveFit['Rms1'])
		cost_func=float(Spectra.CostFunction)
		rms_norm=float(Spectra.CurveFit['Rms2'])
		snr_perc=int(Spectra.SnrPerc)






		tmin=cfg["PlotFigure"]["PreP"]
		tmax=cfg["PlotFigure"]["PostP"]
		cm = 1/2.54  # centimeters in inches
		fig, ax = plt.subplots(4, gridspec_kw={'height_ratios': [1, 1, 1, 10]}, figsize=(16, 20),  constrained_layout=True)
		for k in [0,1,2]:
			ztime = st[k].stats.starttime
			etime= st[k].stats.endtime
			pick=Spectra.Ppick

			if (ztime+pick-tmin) < ztime or (ztime+pick+tmax) > etime:
				tshift=0
				wv=st[k]

				if first_spectra_plot and k == 0:
					console.log("[warning]WARNING:[/warning]  [normal]The spectral plot's window exceeds waveform duration")
					console.print(" ")
				#	console.print(" ")
				#	console.print(" ")
			else:
				tshift=pick-tmin
				wv=st[k].slice(ztime+pick-tmin, ztime+pick+tmax)

			ax[k].plot(wv.times(), wv.data, "-", color='dimgrey')
			ax[k].axvspan(t1_sig-tshift, Pick-tshift, facecolor='orange', alpha=0.5)
			ax[k].axvspan(Pick-tshift, t2_sig-tshift, facecolor='red', alpha=0.4)
			ax[k].axvspan(t1_noise-tshift, t2_noise-tshift, facecolor='darkgrey', alpha=0.5)
			ax[k].set_xticks(np.arange(wv.times()[0], wv.times()[-1], step=1))
			ax[k].tick_params(axis='x', labelsize=16)
		ax[3].loglog(f1_noise,omg1_noise,'.', color='grey', markersize=18)
		#ax[3].set_ylim((10**-16,10**-4))
		ax[3].set_xlim(cfg["PlotFigure"]["FminLim"],cfg["PlotFigure"]["FmaxLim"])
		ax[3].loglog(f1,omg1,'.',color='orangered', markersize=18)
		ax[3].loglog(f1,omg1,'--',color='orangered', markersize=18, label='_nolegend_')

		ax[3].loglog(f1,pred1,'k-', linewidth=4)
		
		ax[3].set_xlabel('Frequency [Hz]', fontweight="bold", size=30)
		ax[3].set_ylabel('Displacement (m/Hz)', fontweight="bold", size=30)
		ax[3].legend(['Noise','Source Spectrum','Best Fit'],loc=3, numpoints=1, fontsize=30)
		plt.xticks(fontsize=30)
		plt.yticks(fontsize=30)
		ax[3].tick_params(direction='out', length=8, which='both', width=3, colors='k', grid_color='k', grid_alpha=0.5)
		fig.suptitle('Sta:%s, LenSig:%.2f, PrePick:%.2f, AfterPick:%.2f, \n Omega:%.3e, fc:%.2f, Q:%.2f, \n Cost Func:%.3e, Rms Curve Fit:%.3e, Rms Norm.:%.3e, \n SNR Perc:%.0f' 
			% (sta, win_dur, len_sig_prePick, len_sig_afterPick, omega0, corn_frq, q_val, cost_func, rms_fit, rms_norm, snr_perc), fontweight="bold", size=20) 



		if not show_figure and not save_figure:
			plt.close()
			break
		
		if show_figure & save_figure:
			plt.savefig(str(Spectra.id)+'.'+str(Spectra.station)+'.png',  bbox_inches='tight')
			plt.show()
			plt.close()
		elif show_figure and not save_figure:
			plt.show()
			plt.close()


		if not show_figure: 
			if save_figure:
				plt.savefig(str(Spectra.id)+'.'+str(Spectra.station)+'.png',  bbox_inches='tight')
				plt.close()

		first_spectra_plot = False


	t1_stop = process_time()
	# print("  ")
	# print("Elapsed time for showing/saving figures in seconds:",
#                                        t1_stop-t1_start) 
	# print("  ")