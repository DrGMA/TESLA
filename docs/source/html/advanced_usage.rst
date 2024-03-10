**Advanced Usage**
==================

TESLA provides advanced options that enable users to fine-tune the spectral analysis process through ad-hoc configuration settings.


**Customizing Configuration**
-----------------------------

Users can modify the configuration settings to customize TESLA's functionality to their specific requirements.
 
In the case of noisy or particularly complex signals, the curve fitting procedure may not yield realistic results due to a lack of convergence of the SciPy ``curve_fit`` routine towards a solution. This results in TESLA not selecting any spectra either because there are none to classify or due to a default classification that discards spectra with unrealistic values for the parameters :math:`\Omega_0`, :math:`F_c` and :math:`Q`, or their associated errors.

For this reason, TESLA allows the option to force the curve fit, enabling the generation of computed spectra with parameter values that may not be correct. Indeed, TESLA allows for the analysis of spectra to recover low-frequency level values (:math:`\Omega_0`), even when realistic parameter values of :math:`F_c` and :math:`Q` are not achievable. In fact, it may happen that the values of :math:`F_c` and :math:`Q` are unconstrained, while the :math:`\Omega_0` value tends to more reliable values, remaining more stable.

To utilize TESLA in this mode, set in the ``Config.yaml``:

.. code-block:: yaml

    SpectraSelection:
        CostFunctionClass: False

When this option is utilized, the evaluation and classification of the spectra are based not on the ``Cost_Function`` but rather on the goodness of the fit, as determined only by the ``RMS_Normalized`` value. Indeed, the classification of the computed spectra using the different signal windows selected, as well as their selection, is based on the ``RMS_Normalized`` value, while the ``Cost_Function`` value is not calculated. In the outputs, its value is deliberately indicated as -999.00.

.. warning::

   When utilizing this function, it is strongly advised to carefully evaluate the results. The calculated spectrum may not accurately represent a theoretical spectrum because the free parameters (:math:`\Omega_0`,:math:`F_c` and :math:`Q`) are not constrained and may not hold realistic values. Caution is recommended when operating TESLA in this mode, as the outcomes may significantly deviate from expected theoretical models of earthquake source spectrum.

**Advanced Usage Example**
--------------------------

 **1. Navigate to the Example Directory**


Within the TESLA repository, the ``examples`` folder contains various examples, including ``example_2``. First, navigate to the example directory using the following command:

.. code-block:: bash

   cd path/to/example_2

Replace ``path/to/example_2`` with the actual path to the example_2 directory on your computer.

 **2. Configuration**


Inside the ``example_2`` directory, you will find a pre-set configuration file (e.g., ``Config_ex2.yaml``). Make sure to review and, if necessary, adjust this file to suit your analysis needs. The configuration file includes crucial parameters affecting the analysis, such as applied filters, temporal windows, and more.

For advanced usage focused on spectra selection, you might want to modify the ``SpectraSelection`` parameter in your configuration file to differently handle the spectra classification. Here's how:

.. code-block:: yaml

    SpectraSelection:
        CostFunctionClass: False

This configuration disables the use of cost function-based classification, allowing instead for spectra selection based solely on the normalized ``RMS_Normalized`` (in other word MAPE).

 **3. Run TESLA**


With the configuration file set, you can start the analysis by running TESLA. The exact command may vary based on your installation, but it generally looks something like this:

.. code-block:: bash

   TESLA -e 201307100 -c Config_ex2.yaml

This command will launch TESLA using the specified configuration file. Navigate to the waveform data directory (e.g., ``201307100``) to review the results.Ensure your Python environment is correctly set up and all TESLA dependencies are installed.
