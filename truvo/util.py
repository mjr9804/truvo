import configparser
from os import path

import nuvo
from zone import Zone

def load_config():
    config = configparser.ConfigParser()
    config.read(path.abspath(path.join(__file__, '../../config.ini')))
    return config

def init_zone(zone, nuvo_input):
    Zone(zone['Name'].capitalize(), zone['ZID'], nuvo_input)

def init_zones():
    nuvo_input = nuvo.AudioInputModule()
    nuvo_audio = nuvo.AudioDistributionModule()
    for zone in nuvo_audio.list_zones():
        init_zone(zone, nuvo_input)
