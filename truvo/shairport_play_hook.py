#!/usr/bin/python3

""" Hook called when shairport-sync starts playing """

import sys

import nuvo
import util

def _main(zone_id):
    config = util.load_config()
    nuvo_audio = nuvo.AudioDistributionModule(config['DEFAULT']['GlobalSourceId'])
    nuvo_audio.play(zone_id)

if __name__ == '__main__':
    _main(sys.argv[1])
