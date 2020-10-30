""" Audio zone module """

from shairport import Shairport

class Zone:
    """ Represents an audio zone in the NuVo system """
    def __init__(self, name, zone_id):
        self.name = name
        self.zone_id = zone_id
        self.number = int(zone_id[-1])
        self.shairport = Shairport(self)
        self.shairport.start()
