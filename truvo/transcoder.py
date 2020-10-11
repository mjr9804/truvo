import threading

import ffmpeg

class Transcoder:
    def __init__(self, stdin=None, **kwargs):
        self.stdin = stdin
        self.stdout = None
        self.input_file = kwargs.get('input_file', 'pipe:')
        self.input_kwargs = {'format': kwargs.get('input_format', 's16le'),
                             'codec': kwargs.get('input_codec', 'pcm_s16le'),
                             'ac': kwargs.get('input_audio_channels', '2')}
        self.output_file = kwargs.get('output_file', 'pipe:1')
        self.output_kwargs = {'format': kwargs.get('output_format', 'mp3'),
                              'codec': kwargs.get('output_codec', 'mp3')}
        self.proc = None

    def start(self):
        self.proc = ffmpeg.input(self.input_file, **self.input_kwargs) \
                        .output(self.output_file, **self.output_kwargs) \
                        .run_async(pipe_stdin=True, pipe_stdout=True)
        self.stdout = self.proc.stdout
        threading.Thread(target=self.proc.communicate, name='Transcoder',
                         kwargs={'input': self.stdin.read()}).start()

    def stop(self):
        self.proc.kill()
        self.proc = None
        self.stdout = None
