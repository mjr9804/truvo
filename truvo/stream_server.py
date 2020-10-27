import subprocess

import util

class StreamServer:
    def __init__(self, zone, stdin=None, **kwargs):
        self.config = util.load_config()
        self.zone = zone
        self.stdin = stdin
        self.codec = kwargs.get('codec', 'mp3')
        self.stream_name = f'{zone.name}.mp3'
        self.listen_ip = self.config['DEFAULT']['ListenAddress']
        self.port = f'800{zone.number}'
        self.cmd = f'cvlc - --sout "#standard{{access=http,mux={self.codec},'
        self.cmd += f'dst={self.listen_ip}:{self.port}/{self.stream_name}}}"'
        self._kill_ancestor()
        self.proc = None

    def _kill_ancestor(self):
        subprocess.run(f"pkill -9 -f '/bin/sh -c {self.cmd}'", shell=True)

    def start(self):
        self.proc = subprocess.Popen(self.cmd, shell=True, stdin=self.stdin)

    def stop(self):
        self.proc.kill()
        self.proc = None
