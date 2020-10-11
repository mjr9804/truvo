import configparser
from os import path

def load_config():
    config = configparser.ConfigParser()
    config.read(path.abspath(path.join(__file__, '../../config.ini')))
    return config
