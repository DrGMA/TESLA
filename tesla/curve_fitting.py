# encoding: utf8
#!/usr/bin/env python

"""
These functions are part of TESLA (A Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- math
- numpy
- scipy
- tesla.class_spectra.Spectra
- warnings 
"""

# Import necessary modules
import numpy as np
from math import sqrt
from tesla.class_spectra import Spectra
from scipy.optimize import curve_fit, differential_evolution, OptimizeWarning, basinhopping
import warnings 


#To suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=OptimizeWarning)



#Define the theoretical function for the source spectra (from Abercrombie 1995)

def SourceSpectraTheo(f1, DC1, fc1, Q):
    """
    Calculate theoretical source spectra.

    Parameters:
        f1 (numpy.ndarray): Array of frequencies.
        DC1 (float): DC amplitude.
        fc1 (float): Corner frequency.
        Q (float): Q factor.

    Returns:
        numpy.ndarray: Calculated source spectra.
    """
    gamma = 1
    n = 2
    n=np.array(n, dtype=float)
    gamma=np.array(gamma, dtype=float)
    f1=np.array(f1, dtype=float)
    b = np.array(-1. * ((np.pi * f1 * tt) / Q), dtype=float)
    return np.array((DC1 * np.e**(b))/(1. + (f1/fc1)**(gamma*n))**(1./gamma),dtype=float)



def calculateSSE(parameterTuple):
    """
    Calculate the Sum of Squared Errors (SSE) between the observed spectrum and a theoretical model.

    Parameters:
    - parameterTuple: A tuple of parameters for the theoretical spectrum model.

    Returns:
    - The SSE as a float.

    Note:
    This function assumes the existence of a globally accessible observed spectrum `omg1`
    and a function `SourceSpectraTheo(f1, *parameterTuple)` that computes the theoretical
    spectrum given a frequency `f1` and model parameters.
    """
    # Calculate the theoretical spectrum for the given parameters
    theo_spctr = SourceSpectraTheo(f1, *parameterTuple)

    # Compute and return the sum of squared differences between the observed and theoretical spectra
    return np.sum((omg1 - theo_spctr) ** 2.0)



def find_optimal_params(ParameterBounds):
    """
    Find the optimal parameters using the differential evolution optimization algorithm.
    
    Parameters:
    - parameterBounds: A list of tuples defining the lower and upper bounds for each parameter
                       to be optimized. Each tuple corresponds to one parameter.

    Returns:
    - An array of optimized parameter values.
    
    Example of parameterBounds input:
    parameterBounds = [
        (9000, 100000),  # Bounds for parameter omega
        (3.0, 50.0),     # Bounds for parameter Fc
        (50, 100)        # Bounds for parameter Q
    ]
    """
    
    # Execute differential evolution algorithm to find optimal parameters
    optimized_params_result = differential_evolution(calculateSSE, ParameterBounds, seed=3)
    
    # Return the optimized parameters
    return optimized_params_result.x



def SpectraFitting(cfg, spectra, phase):
    """
    Perform curve fitting on seismic spectra.

    Parameters:
        cfg (dict): Configuration parameters from the TESLA package.
        spectra (Spectra): Spectra object containing spectral data.
        phase (str): Seismic phase ('P' or 'S').

    Returns:
        Spectra: Spectra object with fitted parameters and updated data.
    """
    # Get configuration parameters
    ParameterBounds=[tuple(cfg["CurveFitting"]["OmegaBounds"]), tuple(cfg["CurveFitting"]["FcBounds"]), tuple(cfg["CurveFitting"]["QBounds"])]
    wind_dur = float(spectra.SigWindTimes[1] - spectra.SigWindTimes[0])
    Fmax = float(cfg["SourceSpectra"]["Fmax"])
    Fmin = 1 / wind_dur
    Fred = spectra.SigFrequencies
    Fred_noise = spectra.NoiseFrequencies
    PHTred = spectra.SigSpectrum
    PHTred_noise = spectra.NoiseSpectrum

    global tt
    global f1
    global omg1

    if phase == 'P':
        tt = spectra.Ptraveltime
    else:
        tt = spectra.Straveltime

    # Filter frequencies within range
    dat = np.column_stack((Fred, np.abs(PHTred)))
    f1 = []
    omg1 = []
    for k in np.arange(0, len(dat[:, 0]), 1):
        if Fmin <= dat[k, 0] <= Fmax:
            f1.append(dat[k, 0])
            omg1.append(dat[k, 1])

    # Filter noise frequencies within range
    dat_noise = np.column_stack((Fred_noise, np.abs(PHTred_noise)))
    f1_noise = []
    omg1_noise = []
    for kk in np.arange(0, len(dat_noise[:, 0]), 1):
        if Fmin <= dat_noise[kk, 0] <= Fmax:
            f1_noise.append(dat_noise[kk, 0])
            omg1_noise.append(dat_noise[kk, 1])


    # by default, differential_evolution completes by calling curve_fit() using parameter bounds
    OptimalParameters = find_optimal_params(ParameterBounds)

    # Curve Fitting
    #popt1, pcov1 = curve_fit(SourceSpectraTheo, f1, omg1, method='trf', bounds=([min(spectra.SigSpectrum), 5, 1], [max(spectra.SigSpectrum), 80, 900]) )
    #popt1,pcov1 = curve_fit(SourceSpectraTheo, f1, omg1,  method='lm', maxfev=300000)
    #popt1,pcov1 = curve_fit(SourceSpectraTheo, f1, omg1,  method='lm', maxfev=300000, p0=(initDC,initFc,initQ,initN))
    #popt1,pcov1 = curve_fit(SourceSpectraTheo, f1, omg1,  method='lm', maxfev=300000, p0=(initDC,initFc,initQ))
    #Basin Hopping
    #minimizer_kwargs = {"method": "L-BFGS-B", "bounds": ParameterBounds}
    #res = basinhopping(calculateSSE, x0=OptimalParameters, niter=200, minimizer_kwargs=minimizer_kwargs)
    #popt1=res.x

    #Last version LM
    popt1,pcov1 = curve_fit(SourceSpectraTheo, f1, omg1,  method='lm', maxfev=300000, p0=OptimalParameters)

    # Parameter Errors Last version
    pcov1 = np.sqrt(np.diag(pcov1))

    # Predicted Spectrum
    #pred1 = SourceSpectraTheo(f1, popt1[0], popt1[1], popt1[2], popt1[3])
    #pred1 = SourceSpectraTheo(f1, popt1[0], popt1[1], popt1[2])
    pred1 = SourceSpectraTheo(f1, *popt1)

    DeltaOmega = np.log10(omg1[0]) - np.log10(omg1[-1])

    # Residuals and RMS (1 type)
    omg1 = np.array(omg1)
    residuals1 = omg1 - pred1
    fres1 = sum(abs(residuals1 / omg1)) / len(omg1)

    # Residuals and RMS (2 type)
    fres11 = sum(abs((omg1 - pred1) / omg1)) / len(omg1)
    RES_fc = fres11 * 100

    # Store results in Spectra object
    Dict = {
        'Omega0': popt1[0],
        'Omega0Err': pcov1[0],
        'Fc': abs(popt1[1]),
        'FcErr': pcov1[1],
        'Q': popt1[2],
        'QErr': pcov1[2],      
        'Rms1': fres1,
        'Rms2': RES_fc,
        'DeltaOmega': DeltaOmega
    }


    spectra.CurveFit = Dict
    spectra.SigSpectrum = omg1
    spectra.NoiseSpectrum = omg1_noise
    spectra.SigFrequencies = f1
    spectra.NoiseFrequencies = f1_noise
    spectra.CalculatedSpectrum = pred1

    return spectra
