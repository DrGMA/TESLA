**Troubleshooting**
===================

This section addresses common issues and provides solutions to frequently encountered problems.

**Common Issues**
-----------------

Here, we highlight some common issues users may face while using TESLA and provide guidance on resolving them. Should you encounter any problem, defect, or bug that is not addressed in this section, please do not hesitate to reach out to me at guidomaria.adinolfi@unito.it for assistance.

**Frequently Asked Questions**
------------------------------

This subsection answers frequently asked questions about TESLA and its usage.

**1. Does TESLA compute the focal mechanism?**

No, TESLA does not compute the focal mechanisms. Instead, TESLA calculates the low-frequency spectral levels, which can be used in addition to P-wave polarities as observables for the computation of fault plane solutions. To achieve this, it is necessary to use specific codes that can process both types of observables. We recommend using BISTROP (`De Matteis et al., 2016 <https://doi.org/10.1785/0220150259>`_) as done in the work by Adinolfi et al. (2023). BISTROP is acknowledged for being both fast and easy to use. The code can be obtained upon request from the `author <mailto:dematt@unisannio.it>`_.

------------------------------

**2. How fast is TESLA in data analysis?**

TESLA is as a fast tool capable of handling large datasets with minimal manual intervention from analysts. Notably, it can compute both P- and S-wave spectra for 10 seismic stations in approximately 23 seconds on a multiprocessor personal computer (Intel Core i5-6400 CPU @ 2.70 GHz × 4, 16 GiB, Ubuntu 22.04.2 LTS). The primary factor that slows TESLA down is the process of saving figures, especially when the option to save all figures, including those for both selected and not-selected spectra, is utilized. Depending on the settings in the configuration file, the calculation of a single spectrum (P or S phase) can involve exploring from tens to a hundred windows, with a figure produced for each one. Therefore, we recommend saving figures only for spectra selected by the algorithm. For a comprehensive understanding or for parameter tuning, user might choose to save all spectra, both selected and not-selected, but we advise doing this for only one or two stations to avoid unnecessary slowdowns. For maximum speed, you can choose not to save any figures, resulting in only CSV file outputs.
