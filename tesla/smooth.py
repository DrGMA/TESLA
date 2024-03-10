# encoding: utf8
"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- numpy
"""

import numpy

def smooth(x, window_len=5, window='hanning'):
    """
    Smooth the data using a window with the requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) at both ends so that transient parts are minimized
    at the beginning and end of the output signal.

    Parameters:
        x (numpy.ndarray): The input signal.
        window_len (int): The dimension of the smoothing window; should be an odd integer.
        window (str): The type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'.
            'flat' window will produce a moving average smoothing.

    Returns:
        numpy.ndarray: The smoothed signal.

    Example:
        t = linspace(-2, 2, 0.1)
        x = sin(t) + randn(len(t)) * 0.1
        y = smooth(x)

    See also:
        numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve,
        scipy.signal.lfilter

    Note:
        Length(output) != Length(input), to correct this:
        return y[int(window_len/2):-int(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1-dimensional arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window must be one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = numpy.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]

    if window == 'flat':  # Moving average
        w = numpy.ones(window_len, 'd')
    else:
        w = eval('numpy.' + window + '(window_len)')

    y = numpy.convolve(w / w.sum(), s, mode='valid')

    return y[int(window_len / 2):-int(window_len / 2)]

    #Original
    #return y
    return y[int(window_len/2):-int(window_len/2)]