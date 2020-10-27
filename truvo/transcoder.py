import subprocess

class Transcoder:
    def __init__(self, stdin=None, **kwargs):
        self.stdin = stdin
        self.stdout = None
        self.input_file = kwargs.get('input_file', '-')
        self.input_kwargs = {'format': kwargs.get('input_format', 's16le'),
                             'codec': kwargs.get('input_codec', 'pcm_s16le'),
                             'ac': kwargs.get('input_audio_channels', '2')}
        self.output_file = kwargs.get('output_file', 'pipe:1')
        self.output_kwargs = {'format': kwargs.get('output_format', 'mp3'),
                              'codec': kwargs.get('output_codec', 'mp3')}
        self.cmd = f'ffmpeg -vn -f {self.input_kwargs["format"]} '
        self.cmd += f'-codec {self.input_kwargs["codec"]} -ac {self.input_kwargs["ac"]} '
        self.cmd += f'-i {self.input_file} -codec {self.output_kwargs["codec"]} '
        self.cmd += f'-f {self.output_kwargs["format"]} {self.output_file} '
        self._kill_ancestor()
        self.proc = None

    def _kill_ancestor(self):
        subprocess.run(f"pkill -9 -f '{self.cmd}'", shell=True)

    def start(self):
        self.proc = subprocess.Popen(self.cmd, shell=True, stdin=self.stdin, stdout=subprocess.PIPE)
        self.stdout = self.proc.stdout

    def stop(self):
        self.proc.kill()
        self.proc = None
        self.stdout = None
