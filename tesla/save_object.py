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

def SaveObject(obj, filename):
    """
    Save an object to a file using pickle.

    Parameters:
        obj (object): The object to be saved.
        filename (str): The filename to save the object to.

    Returns:
        None
    """

    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
