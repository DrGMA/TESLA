**Getting Started**
===================

This section provides instructions for installing TESLA, running the tool, and understanding its basic usage.

**Download**
------------

To download the TESLA package, you have two options:

**Option 1: Download ZIP**

1. Open a web browser and navigate to the `TESLA <https://github.com/DrGMA/TESLA>`_ repository on GitHub.
   
2. On the TESLA repository page, locate the green "Code" button. Click on it to open a dropdown menu.
   
3. In the dropdown menu, click on "Download ZIP" to download the repository as a compressed ZIP file to your computer.
   
4. Extract the contents of the ZIP file to a directory of your choice.

**Option 2: Clone with Git**

1. Open a terminal window.

2. Navigate to the directory where you wish to download the TESLA repository.

3. Execute the following command to clone the TESLA repository:

   .. code-block:: bash

      git clone https://github.com/DrGMA/TESLA.git

After downloading and extracting the repository or cloning it using Git, you can proceed with the installation steps provided in this manual.


**Installation**
----------------

TESLA can be installed using one of the following methods, tailored to different development needs and environments. It's recommended to install TESLA either via a virtual environment or using Anaconda/Conda to avoid conflicts with other package versions installed on your system. For those less experienced, Anaconda/Conda is the preferred option.

**Before proceeding, ensure you have pip installed.** If pip is not installed, refer to the `pip <https://pip.pypa.io/en/stable/installation/>`_ installation guide.


**Option 1: Standard Installation Using pip**

This method installs TESLA directly from the downloaded source directory, making it available system-wide.

.. code-block:: bash

   # Navigate to the directory containing the TESLA folder
   cd path/to/tesla

   # Install TESLA using pip
   pip install ./tesla

**Option 2: Using a Virtual Environment**

Isolating TESLA in a virtual environment prevents conflicts with other projects.

.. code-block:: bash

   # Create a virtual environment named 'tesla_env'
   python -m venv tesla

   # Activate the virtual environment
   # On Windows
   tesla\Scripts\activate
   # On Unix or MacOS
   source tesla/bin/activate

   # Install TESLA
   cd path/to/tesla
   pip install .

**Option 3: Using Anaconda/Conda**

For an isolated setup, install TESLA within a Conda environment. Download `Anaconda/Conda <https://www.anaconda.com/products/individual>`_.

.. code-block:: bash

   # Create and activate a new Conda environment
   conda create --name tesla python=3.8
   conda activate tesla

   #Install pip
   conda install pip

   #Install obspy
   pip install obspy

   # Install TESLA from the source directory
   cd path/to/TESLA
   pip install .

**Editable Installation**

For developers wanting to modify TESLA's code and test changes in real-time, install TESLA in editable mode.

.. code-block:: bash

   # Navigate to the directory containing the TESLA folder
   cd path/to/TESLA

   # Install TESLA in editable mode
   pip install -e ./tesla
   
or

.. code-block:: bash

   pip install -e .


Installing TESLA in editable mode links the installed package directly to the source code so that any modifications are reflected immediately, streamlining the development process.

For beginners or those seeking the simplest setup, Anaconda/Conda is recommended to minimize potential conflicts and issues related to package dependencies.


**Running TESLA**
-----------------

After installing TESLA, you can run the tool by executing specific commands in your terminal. The basic way to run TESLA involves specifying the earthquake ID and the path to your configuration file.

To see all available options, including required and optional arguments, you can use the help command:

.. code-block:: bash

   TESLA -h

This command outputs the usage instructions:

.. code-block:: text

   usage: TESLA [-h] -e EARTHQUAKE_ID -c CONFIGURATION_FILE

   optional arguments:
     -h, --help            show this help message and exit
     -e EARTHQUAKE_ID, --earthquake_id EARTHQUAKE_ID
                           Provide Earthquake Id
     -c CONFIGURATION_FILE, --configuration_file CONFIGURATION_FILE
                           Provide Configuration File

To run TESLA with the required parameters, use the following command structure:

.. code-block:: bash

   TESLA -e path/to/your/earthquake_id_folder -c path/to/your/configuration_file.yaml

These parameters are necessary for running the command effectively.

**Basic Usage**
---------------

To use TESLA effectively, you'll need to specify both the earthquake ID and the configuration file through its command line interface. Here’s a breakdown of these inputs:

- **Earthquake ID**: This is a unique identifier for an earthquake, represented by a folder name that contains the waveform data for analysis. Before executing TESLA, ensure that you've prepared this folder with the waveform data in the correct format required by TESLA.

- **Configuration File**: This file includes all necessary settings and parameters for processing the seismic data with TESLA. It must be properly edited and filled out before starting the analysis, specifying paths, analysis parameters, and any other essential options.

Ensure your data is organized in the required format and that the configuration file is meticulously prepared to meet your specific processing needs. The format for the waveform data and the details required in the configuration file are outlined in the subsequent sections of this manual.

To run TESLA with these considerations in mind, use the following example command:

.. code-block:: bash

   TESLA -e path/to/your/earthquake_id_folder -c path/to/your/configuration_file.yaml

Replace ``path/to/your/earthquake_id_folder`` with the path to the folder containing the waveform data for the earthquake you wish to analyze, and ``path/to/your/configuration_file.yaml`` with the path to your edited configuration file. This ensures TESLA can access and process the seismic data based on the specific instructions provided in the configuration file.

