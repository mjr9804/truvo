import json
import logging
import socket
import traceback

class AudioDistributionModule:
    NUVO_AUDIO_DIST_FQDN = 'ADM1.local'
    NUVO_AUDIO_DIST_PORT = 2112
    NUVO_API_TERMINATOR = b'\x00'

    def __init__(self):
        self.server_ip = socket.gethostbyname(AudioDistributionModule.NUVO_AUDIO_DIST_FQDN)
        self.conn = socket.create_connection((self.server_ip,
                                              AudioDistributionModule.NUVO_AUDIO_DIST_PORT))
        self.analog_source = 'S3'
        self.payload_id = 1

    def _request(self, **kwargs):
        payload = kwargs
        payload['ID'] = self.payload_id
        print(f'sending payload {payload}')
        self.conn.send(json.dumps(payload).encode('utf-8') + \
                       AudioDistributionModule.NUVO_API_TERMINATOR)
        self.payload_id += 1
        return self._response()

    def _response(self):
        data = b''
        while AudioDistributionModule.NUVO_API_TERMINATOR not in data:
            data += self.conn.recv(1)
        res = json.loads(data[:-1])
        print(f'received {res}')
        if res.get('Service') in ['Greeting', 'ping']:
            return self._response()
        return res

    def _set_power(self, zone_id, power_on):
        self._request(Service='SetZoneProperty', ZID=zone_id, PropertyList={'Power': power_on})

    def power_off(self, zone_id):
        self._set_power(zone_id, False)

    def list_zones(self):
        zones = []
        res = self._request(Service='ListZones')
        try:
            return res['ZoneList']
        except Exception as err:
            logging.debug(traceback.format_exc())
            logging.error(err)
        return zones

    def play(self, zone_id):
        print(f'Playing in {zone_id}')
        self._request(Service='SetZoneProperty', ZID=zone_id,
                      PropertyList={'Power': True, 'Source': self.analog_source, 'Volume': 20})
