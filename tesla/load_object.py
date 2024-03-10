# encoding: utf8
#!/usr/bin/env python

"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- pickle
"""

import pickle

def LoadObject(filename, show=True):
    """
    Load an object from a pickle file using TESLA.

    Parameters:
        filename (str): Name of the pickle file to load.
        show (bool): Whether to display object information (default is True).

    Returns:
        object: Loaded object from the pickle file.
    """

    # Open and load the pickle file
    with open(filename, 'rb') as object_file:  
        loaded_object = pickle.load(object_file)
        object_file.close()

    # Display object information if requested
    if show:
        for item in loaded_object:
            print(item.id)
    
    return loaded_object
