import select
import subprocess
import threading
from time import sleep

import util
from nuvo import NuVo

class Shairport:
    def __init__(self, zone_name, zone_instance_id):
        self.zone_name = zone_name
        self.zone_instance_id = zone_instance_id
        self.config = util.load_config()
        self.cfg_path = f'/tmp/shairport_{self.zone_name}.cfg'
        self.config_file = self._build_config()
        self.proc = None
        self.cmd = f'/usr/local/bin/shairport-sync -c {self.cfg_path}'
        listen_address = self.config['DEFAULT']['ListenAddress']
        self.stream_url = f'http://{listen_address}:800{zone_instance_id}/{zone_name}.mp3'
        self.nuvo = NuVo()
        self.playing = False

    def _build_config(self):
        config = 'general = \n{\n'
        config += f'\tname = "{self.zone_name}";\n'
        config += '\toutput_backend = "stdout";\n'
        config += f'\tport = 500{self.zone_instance_id};\n'
        config += '};'
        return config

    def _kill_ancestor(self):
        subprocess.run(f"pkill -9 -f '{self.cmd}'", shell=True)

    def stream_watchdog(self):
        while True:
            ready, _, _ = select.select([self.proc.stdout], [], [], 0)
            if self.proc.stdout in ready and not self.playing:
                self.playing = True
                self.nuvo.set_stream_url(self.zone_instance_id, self.stream_url)
            sleep(0.1)

    def start(self):
        self._kill_ancestor()        
        with open(self.cfg_path, 'w') as cfg_file:
            cfg_file.write(self.config_file)
        proc = subprocess.Popen(self.cmd.split(' '), stdout=subprocess.PIPE)
        self.proc = proc
        threading.Thread(target=self.stream_watchdog, name='Shairport Stream Watchdog').start()
        return proc

