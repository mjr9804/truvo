""" Main script """

import threading

import nuvo
import util
from zone import Zone

if __name__ == '__main__':
    config = util.load_config()
    nuvo_audio = nuvo.AudioDistributionModule(config['DEFAULT']['GlobalSourceId'])
    for zone in nuvo_audio.list_zones():
        zone_name = zone['Name'].capitalize()
        threading.Thread(target=Zone, args=(zone_name, zone['ZID']), name=zone_name).start()
