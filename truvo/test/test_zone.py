"""
Tests for zone.py
"""
#pylint: disable=missing-class-docstring,missing-function-docstring,arguments-differ

from unittest import TestCase
from unittest.mock import patch

from truvo import zone

class TestZone(TestCase):
    @patch('truvo.zone.Shairport')
    def setUp(self, mock_shairport_class):
        self.mock_shairport_class = mock_shairport_class
        self.mock_shairport = mock_shairport_class.return_value
        self.zone_id = 'Z4'
        self.zone_name = 'Kitchen'
        self.zone = zone.Zone(self.zone_name, self.zone_id)

    def test_init(self):
        self.assertEqual(self.zone.name, self.zone_name)
        self.assertEqual(self.zone.zone_id, self.zone_id)
        self.assertEqual(self.zone.number, 4)
        self.assertEqual(self.zone.shairport, self.mock_shairport)
        self.mock_shairport_class.assert_called_with(self.zone)
        self.mock_shairport.start.assert_called()
