import subprocess

class Shairport:
    def __init__(self, zone_name, zone_instance_id):
        self.zone_name = zone_name
        self.zone_instance_id = zone_instance_id
        self.cfg_path = f'/tmp/shairport_{self.zone_name}.cfg'
        self.config = self._build_config()
        self.proc = None
        self.cmd = f'/usr/local/bin/shairport-sync -c {self.cfg_path}'

    def _build_config(self):
        config = 'general = \n{\n'
        config += f'\tname = "{self.zone_name}";\n'
        config += '\toutput_backend = "stdout";\n'
        config += f'\tport = 500{self.zone_instance_id};\n'
        config += '};'
        return config

    def _kill_ancestor(self):
        subprocess.run(f"pkill -9 -f '{self.cmd}'", shell=True)

    def start(self):
        self._kill_ancestor()        
        with open(self.cfg_path, 'w') as cfg_file:
            cfg_file.write(self.config)
        proc = subprocess.Popen(self.cmd.split(' '), stdout=subprocess.PIPE)
        self.proc = proc
        return proc

