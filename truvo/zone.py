import os
import select
from time import sleep

import nuvo
from shairport import Shairport
from stream_server import StreamServer
from transcoder import Transcoder

class Zone:
    def __init__(self, name, zone_id, nuvo_input):
        self.name = name
        self.id = zone_id
        self.number = int(zone_id[-1])
        self.shairport = Shairport(self)
        self.shairport_proc = self.shairport.start()
        self.transcoder = Transcoder(stdin=self.shairport_proc.stdout)
        self.transcoder.start()
        self.stream_server = StreamServer(self, stdin=self.transcoder.stdout)
        self.stream_server.start()
        self.nuvo_input = nuvo_input
        self.nuvo_audio = nuvo.AudioDistributionModule()

    def play_stream(self, stream_url):
        self.nuvo_input.set_stream_url(stream_url)
        self.nuvo_input.play()
        self.nuvo_audio.power_on(self.id)
