#!/usr/bin/python3

import sys

import nuvo

def main(zone_id):
    nuvo_audio = nuvo.AudioDistributionModule()
    nuvo_audio.power_off(zone_id)

if __name__ == '__main__':
    main(sys.argv[1])
