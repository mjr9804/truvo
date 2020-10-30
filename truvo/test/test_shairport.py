"""
Tests for shairport.py
"""
#pylint: disable=missing-class-docstring,missing-function-docstring,arguments-differ,unused-argument
#pylint: disable=protected-access

from unittest import TestCase
from unittest.mock import MagicMock, patch

from truvo import shairport

class TestShairport(TestCase):
    @patch('truvo.util.load_config')
    @patch('subprocess.run')
    def setUp(self, mock_run, mock_load):
        self.mock_run = mock_run
        self.zone = MagicMock()
        self.zone.name = 'Kitchen'
        self.zone.number = 2
        self.zone.zone_id = 'Z2'
        self.mock_config = mock_load.return_value
        self.mock_config['DEFAULT'] = {'OutputDevice': 'usb', 'MixerControlName': 'mix'}
        self.shairport = shairport.Shairport(self.zone)

    @patch('truvo.util.load_config')
    @patch('truvo.shairport.Shairport._build_config')
    @patch('truvo.shairport.Shairport._kill_ancestor')
    def test_init(self, mock_kill, mock_build, mock_load):
        instance = shairport.Shairport(self.zone)
        self.assertEqual(instance.zone, self.zone)
        self.assertEqual(instance.config, mock_load.return_value)
        self.assertEqual(instance.cfg_path, f'/tmp/shairport_{self.zone.name}.cfg')
        self.assertEqual(instance.config_file, mock_build.return_value)
        self.assertEqual(instance.cmd, f'/usr/local/bin/shairport-sync -c {instance.cfg_path}')
        mock_kill.assert_called()

    @patch('truvo.util.get_cwd', return_value='/test')
    def test_build_config(self, mock_cwd):
        start_script = '/test/../shairport_play_hook.py'
        stop_script = '/test/../shairport_stop_hook.py'
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
        config += f'\toutput_device = "{self.mock_config["DEFAULT"]["OutputDevice"]}";\n'
        config += f'\tmixer_control_name = "{self.mock_config["DEFAULT"]["MixerControlName"]}";\n'
        config += '};\n'
        res = self.shairport._build_config()
        self.assertEqual(res, config)

    def test_kill_ancestor(self):
        self.shairport._kill_ancestor()
        self.mock_run.assert_called_with(f"pkill -9 -f '{self.shairport.cmd}'", shell=True,
                                         check=False)

    @patch('builtins.open')
    @patch('subprocess.run')
    def test_start(self, mock_run, mock_open):
        mock_file = mock_open.return_value.__enter__.return_value
        self.shairport.start()
        mock_open.assert_called_with(self.shairport.cfg_path, 'w')
        mock_file.write.assert_called_with(self.shairport.config_file)
        mock_run.assert_called_with(self.shairport.cmd.split(' '), check=True)
