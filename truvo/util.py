import configparser
from os import path

def get_cwd():
    return path.abspath(path.join(__file__, '..'))

def load_config():
    config = configparser.ConfigParser()
    config.read(path.join(get_cwd(), '../config.ini'))
    return config
