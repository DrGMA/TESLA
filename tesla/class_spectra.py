# encoding: utf8
#!/usr/bin/env python

"""
This class is part of TESLA (A Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it
"""

class Spectra:
  """
  Class Spectra for representing a source spectrum.
  """
  def __init__(self, id, station, Ppick, Spick, Ptraveltime, Straveltime, SigWindTimes, NoiseWindTimes, SigFrequencies, SigSpectrum, NoiseFrequencies, NoiseSpectrum, SnrPerc, CurveFit, CalculatedSpectrum, CostFunction):
    self.id = id
    self.station= station
    self.Ppick = Ppick
    self.Spick = Spick
    self.Ptraveltime= Ptraveltime
    self.Straveltime= Straveltime
    self.SigWindTimes = SigWindTimes
    self.NoiseWindTimes = NoiseWindTimes 
    self.SigFrequencies = SigFrequencies
    self.SigSpectrum = SigSpectrum
    self.NoiseFrequencies = NoiseFrequencies
    self.NoiseSpectrum = NoiseSpectrum
    self.SnrPerc = SnrPerc
    self.CurveFit = CurveFit
    self.CalculatedSpectrum = CalculatedSpectrum
    self.CostFunction = CostFunction

  def show(self):
    print('id: ', self.id)
    print('Station: ', self.station)
    print('Ppick: ', self.Ppick)
    print('Spick: ', self.Spick)
    print('Ptraveltime: ', self.Ptraveltime)
    print('Straveltime: ', self.Straveltime)
    print('SNR Percentage: ', self.SnrPerc)
    print('CurveFit: ', self.CurveFit)
    print('Cost Function: ', self.CostFunction)

  def show_all(self):
    print('id: ',self.id)
    print('Ppick: ', self.Ppick)
    print('Spick: ', self.Spick)
    print('Ptraveltime: ', self.Ptraveltime)
    print('Straveltime: ', self.Straveltime)
    print('SigWindTimes: ', self.SigWindTimes)
    print('NoiseWindTimes: ', self.NoiseWindTimes)
    print('SigFrequencies: ', self.SigFrequencies)
    print('SigSpectrum: ', self.SigSpectrum)
    print('NoiseFrequencies: ', self.NoiseFrequencies)
    print('NoiseSpectrum: ', self.NoiseSpectrum)
    print('SNR Percentage: ', self.SnrPerc)
    print('CurveFit: ', self.CurveFit)
    print('Cost Function: ', self.CostFunction)
