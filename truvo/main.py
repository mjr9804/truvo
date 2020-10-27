import threading

import nuvo
from zone import Zone

if __name__ == '__main__':
    nuvo_audio = nuvo.AudioDistributionModule()
    for zone in nuvo_audio.list_zones():
        zone_name = zone['Name'].capitalize()
        threading.Thread(target=Zone, args=(zone_name, zone['ZID']), name=zone_name).start()
