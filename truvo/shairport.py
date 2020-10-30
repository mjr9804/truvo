""" Interact with shairport-sync """

import os
import subprocess

from . import util

class Shairport:
    """ Instance of a shairport-sync process """
    def __init__(self, zone):
        self.zone = zone
        self.config = util.load_config()
        self.cfg_path = f'/tmp/shairport_{zone.name}.cfg'
        self.config_file = self._build_config()
        self.cmd = f'/usr/local/bin/shairport-sync -c {self.cfg_path}'
        self._kill_ancestor()

    def _build_config(self):
        start_script = os.path.join(util.get_cwd(), '../shairport_play_hook.py')
        stop_script = os.path.join(util.get_cwd(), '../shairport_stop_hook.py')
        config = 'general = \n{\n'
        config += f'\tname = "{self.zone.name}";\n'
        config += '\toutput_backend = "alsa";\n'
        config += f'\tport = 500{self.zone.number};\n'
        config += '\tvolume_range_db = 30;\n'
        config += '};\n'
        config += 'sessioncontrol = \n{\n'
        config += f'\trun_this_before_play_begins = "{start_script} {self.zone.zone_id}";\n'
        config += f'\trun_this_after_play_ends = "{stop_script} {self.zone.zone_id}";\n'
        config += '};\n'
        config += 'alsa = \n{\n'
        config += f'\toutput_device = "{self.config["DEFAULT"]["OutputDevice"]}";\n'
        config += f'\tmixer_control_name = "{self.config["DEFAULT"]["MixerControlName"]}";\n'
        config += '};\n'
        return config

    def _kill_ancestor(self):
        subprocess.run(f"pkill -9 -f '{self.cmd}'", shell=True, check=False)

    def start(self):
        """ Starts the shairport-sync subprocess """
        with open(self.cfg_path, 'w') as cfg_file:
            cfg_file.write(self.config_file)
        subprocess.run(self.cmd.split(' '), check=True)
