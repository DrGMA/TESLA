**Using TESLA with an Earthquake Data Example**
===============================================

This guide provides step-by-step instructions on how to analyze seismic data using TESLA with an earthquake data example included in the TESLA GitHub package.

**Navigate to the Example Directory**
-------------------------------------

First, open a terminal on your computer. If you have already cloned the TESLA GitHub repository, navigate to the example directory using the following command:

.. code-block:: bash

   cd path/to/example_1

Replace ``path/to/example_1`` with the actual path to the example directory on your computer. Within the TESLA repository, the ``examples`` folder contains various examples, including ``example_1``.

**Configuration**
-----------------

Inside the ``example_1`` directory, you will find a pre-set configuration file (e.g., ``Config_ex1.yaml``). Ensure to review and, if necessary, adjust this file to suit your analysis needs. The configuration file includes crucial parameters affecting the analysis, such as applied filters, temporal windows, and more.

**Run TESLA**
-------------

With the configuration file set, you can start the analysis by running TESLA. The exact command may vary based on your installation, but it generally looks something like this:

.. code-block:: bash

   TESLA -e 201307120 -c Config_ex1.yaml

This command will launch TESLA using the specified configuration file. Ensure your Python environment is correctly set up and all TESLA dependencies are installed.

**Check the Results**
---------------------

After the analysis is complete, TESLA will generate the output in the previously explained directory structure. Navigate to the waveform data directory (e.g., ``201307120``) to review the results. You will find the `P` and `S` folders for the analysis of P and S waves, respectively. Inside these folders, for each analyzed station specified in the configuration file, there will be `sel_spectra` and `not_sel_spectra` subfolders containing the selected and unselected spectra, respectively.

Review the figures and CSV files in the `sel_spectra` folders to see the spectra that passed the selection criteria and their spectral fit parameters. These results will provide you with in-depth insights into the quality and characteristics of the analyzed spectra.

This example offers a basic overview of initiating an analysis with TESLA using sample data. Remember, each step may require customizations based on your specific data and research objectives.
