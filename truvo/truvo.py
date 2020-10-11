import subprocess

import util
from shairport import Shairport
from zone import Zone

def init_zones(zones):
    for zone_name, zone_config in zones.items():
        Zone(zone_name, zone_config['instanceid'])

def load_config():
    config = util.load_config()
    config.zones = {zone_name: dict(config[zone_name].items()) for zone_name in config.sections()}
    return config

if __name__ == '__main__':
    config = load_config()
    init_zones(config.zones)
