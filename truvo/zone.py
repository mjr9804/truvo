import os
import select
from time import sleep

from shairport import Shairport
from stream_server import StreamServer
from transcoder import Transcoder

class Zone:
    def __init__(self, zone_name, zone_instance_id):
        self.zone_name = zone_name
        self.zone_instance_id = zone_instance_id
        self.shairport = Shairport(zone_name, zone_instance_id)
        self.shairport_proc = self.shairport.start()
        self.transcoder = Transcoder(stdin=self.shairport_proc.stdout)
        self.transcoder.start()
        self.stream_server = StreamServer(zone_name, zone_instance_id, stdin=self.transcoder.stdout)
        self.stream_server.start()
