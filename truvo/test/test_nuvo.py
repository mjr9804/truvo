"""
Tests for nuvo.py
"""
#pylint: disable=arguments-differ,missing-class-docstring,missing-function-docstring
#pylint: disable=protected-access

import json
from unittest import TestCase
from unittest.mock import patch

from truvo import nuvo

class TestNuvo(TestCase):
    @patch('socket.create_connection')
    @patch('socket.gethostbyname')
    def setUp(self, mock_gethost, mock_create):
        self.mock_gethost = mock_gethost
        self.mock_gethost.return_value = '10.1.1.1'
        self.mock_create = mock_create
        self.mock_conn = self.mock_create.return_value
        self.global_source = 'S3'
        self.adm = nuvo.AudioDistributionModule(self.global_source)

    def test_init(self):
        self.mock_gethost.assert_called_with(nuvo.AudioDistributionModule.NUVO_AUDIO_DIST_FQDN)
        self.assertEqual(self.adm.server_ip, self.mock_gethost.return_value)
        self.mock_create.assert_called_with((self.mock_gethost.return_value,
                                            nuvo.AudioDistributionModule.NUVO_AUDIO_DIST_PORT))
        self.assertEqual(self.adm.conn, self.mock_conn)
        self.assertEqual(self.adm.global_source, self.global_source)
        self.assertEqual(self.adm.payload_id, 1)

    @patch('truvo.nuvo.AudioDistributionModule._response')
    def test_request(self, mock_res):
        payload = {'a': 1, 'ID': 1}
        res = self.adm._request(a=1)
        self.mock_conn.send.assert_called_with(
            json.dumps(payload).encode('utf-8') +  nuvo.AudioDistributionModule.NUVO_API_TERMINATOR
        )
        self.adm.payload_id = 2
        self.assertEqual(res, mock_res.return_value)

    def test_response(self):
        self.mock_conn.recv.side_effect = [b'{', b'"', b'a', b'"', b':', b'1', b'}',
                                           nuvo.AudioDistributionModule.NUVO_API_TERMINATOR]
        res = self.adm._response()
        self.assertEqual(len(self.mock_conn.recv.mock_calls), 8)
        self.assertEqual(res, {'a': 1})

    def test_response_ping(self):
        resp = {'Service': 'ping'}
        side_effect = [char.encode('utf-8') for char in json.dumps(resp)]
        side_effect += [nuvo.AudioDistributionModule.NUVO_API_TERMINATOR,
                        b'{', b'"', b'a', b'"', b':', b'1', b'}',
                        nuvo.AudioDistributionModule.NUVO_API_TERMINATOR]
        self.mock_conn.recv.side_effect = side_effect
        res = self.adm._response()
        self.assertEqual(res, {'a': 1})

    def test_response_greeting(self):
        resp = {'Service': 'Greeting'}
        side_effect = [char.encode('utf-8') for char in json.dumps(resp)]
        side_effect += [nuvo.AudioDistributionModule.NUVO_API_TERMINATOR,
                        b'{', b'"', b'a', b'"', b':', b'1', b'}',
                        nuvo.AudioDistributionModule.NUVO_API_TERMINATOR]
        self.mock_conn.recv.side_effect = side_effect
        res = self.adm._response()
        self.assertEqual(res, {'a': 1})

    @patch('truvo.nuvo.AudioDistributionModule._request')
    def test_set_power(self, mock_req):
        self.adm._set_power('Z1', False)
        mock_req.assert_called_with(Service='SetZoneProperty', ZID='Z1',
                                    PropertyList={'Power': False})

    @patch('truvo.nuvo.AudioDistributionModule._set_power')
    def test_power_off(self, mock_set):
        self.adm.power_off('Z2')
        mock_set.assert_called_with('Z2', False)

    @patch('truvo.nuvo.AudioDistributionModule._request')
    def test_list_zones(self, mock_req):
        mock_req.return_value = {'ZoneList': 'a'}
        res = self.adm.list_zones()
        mock_req.assert_called_with(Service='ListZones')
        self.assertEqual(res, 'a')

    @patch('truvo.nuvo.AudioDistributionModule._request')
    def test_list_zones_fail(self, mock_req):
        mock_req.return_value = {'a': 1}
        res = self.adm.list_zones()
        mock_req.assert_called_with(Service='ListZones')
        self.assertEqual(res, [])

    @patch('truvo.nuvo.AudioDistributionModule._request')
    def test_play(self, mock_req):
        self.adm.play('Z1')
        mock_req.assert_called_with(Service='SetZoneProperty', ZID='Z1',
                                    PropertyList={'Power': True, 'Source': self.adm.global_source,
                                                  'Volume': 50})
