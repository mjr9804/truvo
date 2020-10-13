import subprocess

import nuvo
import util
from shairport import Shairport
from zone import Zone

def init_zones(nuvo_input):
    nuvo_audio = nuvo.AudioDistributionModule()
    for zone in nuvo_audio.list_zones():
        Zone(zone['Name'].capitalize(), zone['ZID'], nuvo_input)

if __name__ == '__main__':
    NUVO_INPUT = nuvo.AudioInputModule()
    init_zones(NUVO_INPUT)
