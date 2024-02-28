# -----------------------------------------------------------------------------
# Congifuration file parsing and setup. Configuration is accessible through
# module variable CONFIG.
#
# Released under WHAT LICENSE?
# email info-comphcilab@umich.edu
# -----------------------------------------------------------------------------

import configparser
import sys
import os.path
import os

def create_config(config_file=None):

    if config_file is None:
        config_file = 'semantic_search_app/config.ini'

    parser = configparser.ConfigParser()

    if not os.path.exists(config_file):
        print('Configuration file ' + config_file + ' does not exist.')

    parser.read(config_file)

    return parser

CONFIG = create_config()
