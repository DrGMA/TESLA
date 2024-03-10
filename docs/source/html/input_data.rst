**Input Data**
==============


TESLA requires waveform data and a configuration file as input. This section explains the format of the input data.

**Waveform Data**
-----------------

Waveform data should be provided in SAC format and organized within a directory.

1. When using SAC files in TESLA, make sure they follow this naming convention:

   - For Z-component: ``{event_id}.{station_name}.1.Z.SAC``
   - For N-component: ``{event_id}.{station_name}.2.N.SAC``
   - For E-component: ``{event_id}.{station_name}.3.E.SAC``

2. These files should be organized within a directory, where the directory name corresponds to the event ID (e.g., ``201307120``). The directory containing the SAC waveform files should ideally be named with a unique identifier that corresponds to a specific seismic event.

Here's an example of how the directory structure might look:

.. code-block:: none

   - MainDirectory/
       - 201307120/       <-- Directory named after the seismic event ID
           - 201307120.SGT00.1.Z.SAC
           - 201307120.SGT00.2.N.SAC
           - 201307120.SGT00.3.E.SAC
           - ... (other waveform files)

3. Each SAC file should contain essential information like P- and S-arrival times, station coordinates (longitude and latitude), event coordinates, and component code. The corresponding header fields ensure that the SAC files are properly structured and contain the necessary metadata for accurate spectral analysis within TESLA. SAC file should contain the following essential information in their header fields:

   - ``stla`` and ``stlo``: The latitude and longitude of the station.
   - ``evla``, ``evlo``, and ``evdp``: The latitude, longitude, and depth of the seismic event.
   - ``kstnm``: The station name.
   - ``kcmpnm``: The component code (Z, N, or E) indicating the vertical, north, or east component.
   - ``a`` (P-arrival time) and ``t0`` (S-arrival time): The P-arrival time and S-arrival time, respectively, should be provided to accurately align the waveforms.

You can customize the SAC file extension in the YAML configuration file under the ``files/ext`` section. This allows you to use a different file extension if needed, though it's recommended to stick with the standard "SAC" in uppercase or "sac" in lowercase for compatibility. Make sure that the file extension set in the configuration file matches the extension of the SAC files. Otherwise, TESLA will not be able to read the SAC files. The SAC files must have the same number of data points (samples) for all three components, ensuring consistent waveform lengths. If this condition is not met, the seismic station will be skipped. Additionally, both the P and S picks must be specified for each station; if either is missing, the station will be skipped. Furthermore, the waveform data must be converted to physical units of velocity, specifically in meters per second (m/s). Only velocity data can be used by TESLA for analysis. Waveforms used for analysis with TESLA must be pre-corrected for instrumental response to represent true ground velocity signals. TESLA does not perform this correction automatically, so data preparation must include this crucial step to ensure the analysis is based on accurate ground motion representation.

**Configuration File**
----------------------

The TESLA configuration file, named ``Config.yaml``, incorporates a variety of settings and parameters essential for operating TESLA. This configuration facilitates customization in terms of window lengths, frequency ranges, and additional analysis preferences, segmented into various sections for targeted aspects of the analysis.

**File Settings**

The ``Files`` section in the configuration file specifies the input waveform data files and their format.

- **stations**: Identifies the list of station name codes with available waveform data, aligning with the seismic stations utilized in the analysis. The waveform data for each station should adhere to the established naming convention.
- **ext**: Defines the file extension for the SAC waveform data files. TESLA will search for files with this extension within the designated directory.

**Crustal Model Settings**

The ``CrustalModel`` section outlines the crustal model parameters used in the analysis.

- **Vp**: Specifies the P-wave velocity (in km/s) within the crustal model.
- **Vs**: Indicates the S-wave velocity (in km/s) within the crustal model.

**Waveform Processing Settings**

The ``WaveformProcessing`` section delineates the parameters governing the waveform data processing.

- **fmin**: The minimum corner frequency (in Hz) for the bandpass filter in signal analysis.
- **fmax**: The maximum corner frequency (in Hz) for the bandpass filter in signal analysis.
- **MinDurSig**: The minimum duration (in seconds) for analyzed signal windows. Signal windows with a duration less than  ``MinDurSig`` are not analyzed.
- **MinLength**: The minimum signal length (in seconds) post-pick time required for analysis. It must be less than or equal to ``MinDurSig``.
- **MaxLength**: The maximum signal length (in seconds) for analysis, post-``MinLength`` and pre-pick time.
- **WindShift**: The incremental step (in seconds) used to expand the signal window during analysis.

**Source Spectra Settings**

The ``SourceSpectra`` section configures the spectral analysis of source spectra.

- **Phase**: Lists the seismic phases for which to perform spectral analysis, with options ``P`` and ``S``. Select either one or both.
- **SnrThr**: Sets the signal-to-noise ratio (SNR) threshold for each frequency within the range for which the SNR is computed.
- **SnrFmax**: The maximum frequency (in Hz) considered for SNR calculation.
- **SnrPerc**: The percentage threshold for validating a spectrum based on SNR. A spectrum is considered valid if its SNR exceeds the ``SnrThr`` for at least ``SnrPerc`` % of the analyzed frequencies.
- **Fmin**: The minimum frequency (in Hz) for spectral fitting.
- **Fmax**: The maximum frequency (in Hz) for spectral fitting.
- **Padding**: The window length (in seconds) used for padding before spectrum calculation.
- **Smoothing**: The number of points used for smoothing the observed spectrum.

**Curve Fitting Settings**

The ``CurveFitting`` section discusses the parameters for the curve fitting process.

- **CostFunctionClass**: This parameter determines if the ``Cost_Function`` is used for seismic source spectra classification (when ``True``). When set to ``False``, the selection is based on fit quality, measured by the ``RMS_Normalized`` (or MAPE).
- **OmegaBounds**: Establishes the search bounds for the initial value of :math:`\Omega_0` (low frequency spectral level) for the spectral fitting process using the Levenberg-Marquardt algorithm.
- **FcBounds**: Establishes the search bounds for the initial value of the :math:`F_c` (corner frequency) for the spectral fitting process using the Levenberg-Marquardt algorithm.
- **QBounds**: Establishes the search bounds for the initial value of :math:`Q` (quality factor) for the spectral fitting process using the Levenberg-Marquardt algorithm.
- **PreFc**: The number of points a computed spectrum must have before the corner :math:`F_c`. If this condition is not met, the spectrum will be discarded.

**Spectra Selection Settings**

The ``SpectraSelection`` section outlines the criteria for selecting optimal source spectra.

- **DeltaOmegaThr**: Threshold for evaluating the amplitude's decreasing trend in the computed spectra. Spectra that do not show a decrease equal to or greater than the difference between the first point's and the last point's ordinates will be discarded 
- **RmsNormThr**: Threshold for the maximum acceptable Mean Absolute Percentage Error (MAPE) for fit assessment. Spectra with a MAPE smaller than this threshold will be selected; others will be discarded.
- **Quant**: The quantile value used for selecting the most accurate source spectra based on their ``Cost_Function`` values. Source spectra with a ``Cost_Function`` value lower than the selected quantile will be chosen; others will be discarded. 

**Plot Figure Settings**

The ``PlotFigure`` section details the parameters for generating and saving source spectra plots.

- **PreP**: The seconds plotted before the P-Pick time.
- **PostP**: The seconds plotted after the P-Pick time.
- **FminLim**: The frequency limit for spectra plots.
- **FmaxLim**: The maximum frequency limit for spectra plots.
- **OnlySpectraSel**: If ``True`` decides if only selected spectra figures are saved. If False, even those not selected will be plotted.
- **ShowFigure**: Determines if the generated figures are displayed.
- **SaveFigure**: Decides if the figures of computed spectra are saved.

**Save Result Settings**

The ``SaveResult`` section allows control over saving computed spectra as pickle objects.

- **SaveObject**: Toggles saving the computed spectra as pickle objects.

This configuration flexibility enhances TESLA's adaptability, allowing users to tailor the visualization and preservation of computed source spectra to their specific requirements.
