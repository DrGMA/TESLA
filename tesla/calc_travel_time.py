# encoding: utf8
#!/usr/bin/env python

"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- math
- obspy
"""

# Import necessary modules
from obspy import read
from math import sqrt

def CalcTravelTime(cfg, wvfrm, phase):
    """
    Calculate travel time of seismic waves.

    Parameters:
        cfg (dict): Configuration parameters from the TESLA package.
        wvfrm (obspy.Stream): Seismic waveform.
        phase (str): Seismic phase ('P' or 'S').

    Returns:
        float: Calculated travel time.
    """
    Vp = cfg["CrustalModel"]["Vp"]
    Vs = cfg["CrustalModel"]["Vs"]

    # tr = read(wvfrm)  # Uncomment this line if 'wvfrm' needs to be read using ObsPy
    tr = wvfrm  # Use the provided waveform directly

    depth = tr[0].stats.sac.evdp
    Repi = tr[0].stats.sac.dist
    Rhypo = sqrt(((Repi**2) + (depth**2)))

    if phase == 'P':
        tt = Rhypo / Vp
    else:
        tt = Rhypo / Vs

    return tt
