import json
import logging
import socket
import traceback

import upnpclient

def discover_device():
    devices = upnpclient.discover(timeout=2)
    try:
        device = [device for device in devices if 'NuVo' in device.friendly_name][0]
        return device
    except IndexError:
        return None

class AudioInputModule:
    def __init__(self):
        self.device = discover_device()
        self.api = self.device.AVTransport

    def set_stream_url(self, url):
        self.api.SetAVTransportURI(InstanceID=0, CurrentURI=url, CurrentURIMetaData='')

    def play(self):
        self.api.Play(InstanceID=0, Speed='1')

class AudioDistributionModule:
    NUVO_AUDIO_DIST_FQDN = 'ADM1.local'
    NUVO_AUDIO_DIST_PORT = 2112
    NUVO_API_TERMINATOR = b'\x00'

    def __init__(self):
        self.server_ip = socket.gethostbyname(AudioDistributionModule.NUVO_AUDIO_DIST_FQDN)
        self.conn = socket.create_connection((self.server_ip,
                                              AudioDistributionModule.NUVO_AUDIO_DIST_PORT))

    def _request(self, **kwargs):
        payload = kwargs
        payload['ID'] = 1
        self.conn.send(json.dumps(payload).encode('utf-8') + \
                       AudioDistributionModule.NUVO_API_TERMINATOR)

    def _response(self):
        data = b''
        while AudioDistributionModule.NUVO_API_TERMINATOR not in data:
            data += self.conn.recv(1)
        res = json.loads(data[:-1])
        if res.get('Service') in ['Greeting', 'ping']:
            return self._response()
        return res

    def _set_power(self, zone_id, power_on):
        self._request(Service='SetZoneProperty', ZID=zone_id,
                      PropertyList={'Power': power_on, 'Source': 'S1'})

    def power_on(self, zone_id):
        self._set_power(zone_id, True)

    def power_off(self, zone_id):
        self._set_power(zone_id, False)

    def list_zones(self):
        zones = []
        self._request(Service='ListZones')
        try:
            return self._response()['ZoneList']
        except Exception as err:
            logging.debug(traceback.format_exc())
            logging.error(err)
        return zones
