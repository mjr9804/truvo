import subprocess
import threading

import util

class StreamServer:
    def __init__(self, zone_name, zone_instance_id, stdin=None, **kwargs):
        self.config = util.load_config()
        self.zone_name = zone_name
        self.zone_instance_id = zone_instance_id
        self.stdin = stdin
        self.codec = kwargs.get('codec', 'mp3')
        self.stream_name = f'{zone_name}.mp3'
        self.listen_ip = self.config['DEFAULT']['ListenAddress']
        self.port = f'800{zone_instance_id}'
        self.cmd = f'cvlc - --sout "#standard{{access=http,mux={self.codec},'
        self.cmd += f'dst={self.listen_ip}:{self.port}/{self.stream_name}}}"'
        self.proc = None

    def start(self):
        self.proc = subprocess.Popen(self.cmd, shell=True)
        threading.Thread(target=self.proc.communicate, name='StreamServer',
                         kwargs={'input': self.stdin.read()}).start()

    def stop(self):
        self.proc.kill()
        self.proc = None
