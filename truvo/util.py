""" Helper functions """

import configparser
from os import path

def get_cwd():
    """ Returns the current working directory as an absolute path """
    return path.abspath(path.join(__file__, '..'))

def load_config():
    """ Load the config file """
    config = configparser.ConfigParser()
    config.read(path.join(get_cwd(), '../config.ini'))
    return config
