from shairport import Shairport

class Zone:
    def __init__(self, name, zone_id):
        self.name = name
        self.id = zone_id
        self.number = int(zone_id[-1])
        self.shairport = Shairport(self)
        self.shairport.start()
