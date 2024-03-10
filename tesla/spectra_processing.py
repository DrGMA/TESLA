# encoding: utf8
"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- math
- matplotlib
- numpy
- obspy
- tesla.smooth 
- tesla.class_spectra
- tesla.calc_travel_time
"""

from obspy.core import trace
from tesla.smooth import smooth
from tesla.class_spectra import Spectra
from tesla.calc_travel_time import CalcTravelTime
import numpy as np
from math import sqrt
from matplotlib import pyplot as plt


def SpectraProcessing(cfg, id, st, i, j, sta, phase):
    """
    Perform Spectra Processing on seismic data.

    Parameters:
        cfg (dict): Configuration settings.
        id (int): Identifier for the processing.
        st (Stream): Seismic data stream.
        i (float): Start time window for processing.
        j (float): End time window for processing.
        sta (str): Station identifier.
        phase (str): Seismic phase ('P' or 'S').

    Notes:
        - This function performs Spectra Processing on seismic data, including signal padding, spectrum calculation, and more.
        - This function modifies the input seismic data stream 'st'.
    """

    if phase == 'P':
        P = st[0].stats.sac.a
        S = st[0].stats.sac.t0
        Pick = P
    else:
        P = st[0].stats.sac.a
        S = st[0].stats.sac.t0
        Pick = S


    for c in [0, 1, 2]:
        T = st[c].data

        # --- Signal --- #
        pht = trace.Trace()
        sampRate = st[c].stats.sampling_rate
        delta = st[0].stats.delta
        pht.stats.sampling_rate = sampRate
        pht.stats.delta = delta

        # --- Signal Padding --- #
        win_dur = ((Pick + j)) - ((Pick - i))
        tot_len = cfg["SourceSpectra"]["Padding"]
        pad_len_sec = (tot_len - win_dur) / 2
        pad_len_pts = int(pad_len_sec / pht.stats.delta)
        pht.data = T[int((Pick - i) * sampRate):int((Pick + j) * sampRate)]
        pht.detrend(type='demean')
        pht.detrend(type='linear')
        pht.taper(type='hann', max_percentage=0.05)
        pht.data = np.pad(pht.data, (pad_len_pts, pad_len_pts), mode='constant')
        pht.stats.npts = len(pht.data)

        # --- Signal Spectrum --- #
        PHT = np.fft.fft(pht.data)
        N = len(pht.data)
        PHT = PHT * (2. / N)
        PHTred = PHT[1:int(len(PHT) / 2 - 1)]
        F = np.fft.fftfreq(pht.stats.npts, pht.stats.delta)
        Fred = F[1:int(len(F) / 2 - 1)]

        # --- Signal Spectrum Division for Omega (displacement in frequency domain) --- #
        PHTred = PHTred / (2 * np.pi * Fred)

    #-----------------------------------------------------------------------------#
    #--Noise---#
        
        noise = trace.Trace()
        noise.stats.sampling_rate = sampRate
        noise.stats.delta = delta

        #---Noise/Padding---#
        if phase=="P":
            noise.data=T[int((P-i-win_dur)*sampRate):int((P-i)*sampRate)]
        else:
            noise.data=T[int((P-win_dur)*sampRate):int((P)*sampRate)]

        noise.detrend(type='demean')
        noise.detrend(type='linear')        
        noise.taper(type='hann',max_percentage=0.05)
        pad_len_sec_noise=(tot_len-win_dur)/2
        pad_len_pts_noise=int(pad_len_sec/pht.stats.delta)
        noise.data=np.pad(noise.data, (pad_len_pts_noise,pad_len_pts_noise), mode='constant')

        noise.stats.npts = len(noise.data)

        #---Noise/Spectrum---#
        PHT_noise = np.fft.fft(noise.data)
        N_noise=len(noise.data)
        PHT_noise = PHT_noise*(2./N_noise)
        PHTred_noise = PHT_noise[1:int(len(PHT_noise)/2-1)]
        F_noise = np.fft.fftfreq(noise.stats.npts, noise.stats.delta)
        Fred_noise = F_noise[1:int(len(F_noise)/2-1)]

        #---Signal/Spectrum/Div for Omega to have displacement in frequency domain---#
        PHTred_noise=PHTred_noise/(2 * np.pi * Fred_noise) 

    #-----------------------------------------------------------------------------#

        if c == 0:
            ZZ=np.abs(PHTred)
            ZZ_noise=np.abs(PHTred_noise)
        if c == 1:
            NN=np.abs(PHTred)
            NN_noise=np.abs(PHTred_noise)
        if c == 2:
            EE=np.abs(PHTred)
            EE_noise=np.abs(PHTred_noise)

    #-----------------------------------------------------------------------------#

    PHTred=[]
    for ll in range(len(ZZ)):
        vett=sqrt((np.power(ZZ[ll],2)+np.power(NN[ll],2)+np.power(EE[ll],2)))
        PHTred.append(vett)

    PHTred_noise=[]
    for lll in range(len(ZZ_noise)):
        vett_noise=sqrt((np.power(ZZ_noise[lll],2)+np.power(NN_noise[lll],2)+np.power(EE_noise[lll],2)))
        PHTred_noise.append(vett_noise)
    #-----------------------------------------------------------------------------#

    #Smoothing
    PHTred=smooth(np.array(PHTred),cfg["SourceSpectra"]["Smoothing"])
    PHTred_noise=smooth(np.array(PHTred_noise),cfg["SourceSpectra"]["Smoothing"])
    #-----------------------------------------------------------------------------#


    #Calculus of the SNR
    goodFreq=[]
    freqExpl=[]
    countFreq=0
        
    for jk in np.arange(0,len(Fred),1):
        if Fred[jk] <= cfg["SourceSpectra"]["SnrFmax"]:
            freqExpl.append(PHTred[jk])
            if (PHTred[jk]/PHTred_noise[jk]) >= cfg["SourceSpectra"]["SnrThr"]:
                countFreq += 1
                goodFreq.append(PHTred[jk]) 

    PercSnr=(countFreq/len(freqExpl))*100
    #-----------------------------------------------------------------------------#

    #Calculate the travel time
    tt=CalcTravelTime(cfg,st,phase)

    if phase=='P':
        Ptraveltime=tt
        Straveltime=[]
    else:
        Ptraveltime=[]
        Straveltime=tt
    #-----------------------------------------------------------------------------#

    #Store the results in the Class Spectra
    Ppick=P 
    Spick=S
    #station=st[0].stats.station
    station=sta
    SigWindTimes=[Pick-i, Pick+j]
    if phase=="P":
        NoiseWindTimes=[P-i-win_dur, P-i]
    else:
        NoiseWindTimes=[P-win_dur, P]
    SigFrequencies=Fred
    SigSpectrum=PHTred
    NoiseFrequencies=Fred_noise 
    NoiseSpectrum=PHTred_noise
    CurveFit=[]
    CalculatedSpectrum=[]
    CostFunction=[]



    spectra=Spectra(id,station,Ppick,Spick,Ptraveltime,Straveltime,SigWindTimes,NoiseWindTimes, 
                SigFrequencies,SigSpectrum,NoiseFrequencies,NoiseSpectrum,PercSnr,CurveFit,CalculatedSpectrum,CostFunction)

    return spectra
