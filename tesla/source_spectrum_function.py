# encoding: utf8
"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- numpy
"""

import numpy as np

tt = []

def SourceSpectraTheo(f1, DC1, fc1, Q):
    """
    Define the theoretical function for the source spectra (from Abercrombie 1995).

    Parameters:
        f1 (numpy.ndarray): Frequency values.
        DC1 (float): Amplitude scaling factor.
        fc1 (float): Corner frequency.
        Q (float): Quality factor.

    Returns:
        numpy.ndarray: Theoretical source spectra.

    Note:
        This function is based on the formula from Abercrombie 1995.
    """
    gamma1 = 1
    n1 = 2
    f1 = np.asarray(f1)
    b = -1. * ((np.pi * f1 * tt) / Q)
    return (DC1 * np.e ** (b) / (1. + (f1 / fc1) ** (gamma1 * n1)) ** (1. / gamma1))
