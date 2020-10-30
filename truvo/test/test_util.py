"""
Tests for util.py
"""
#pylint: disable=missing-class-docstring,missing-function-docstring

from unittest import TestCase
from unittest.mock import patch

from truvo import util

class TestUtil(TestCase):
    @patch('os.path.abspath')
    @patch('os.path.join')
    def test_get_cwd(self, mock_join, mock_abspath):
        res = util.get_cwd()
        self.assertTrue(mock_join.mock_calls[0][1][0].endswith('truvo/util.py'))
        self.assertEqual(mock_join.mock_calls[0][1][1], '..')
        mock_abspath.assert_called_with(mock_join.return_value)
        self.assertEqual(res, mock_abspath.return_value)

    @patch('configparser.ConfigParser')
    @patch('os.path.join')
    @patch('truvo.util.get_cwd')
    def test_load_config(self, mock_cwd, mock_join, mock_parser):
        res = util.load_config()
        mock_join.assert_called_with(mock_cwd.return_value, '../config.ini')
        mock_parser.return_value.read.assert_called_with(mock_join.return_value)
        self.assertEqual(res, mock_parser.return_value)
