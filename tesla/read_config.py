# encoding: utf8
#!/usr/bin/env python

"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- yaml
"""

import yaml
import os

def import_config(Config_file, print_cfg=False):
    """
    Import the configuration file in YAML format and return the configuration dictionary.
    
    Parameters:
        print_cfg (bool): Whether to print the loaded configuration (default: False).
        
    Returns:
        dict: The loaded configuration dictionary.
    """



    with open(Config_file, "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        
        if print_cfg:
            print(yaml.dump(cfg))

        return cfg
