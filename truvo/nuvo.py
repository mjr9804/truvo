""" Interact with the NuVo system """

import json
import logging
import socket
import traceback

class AudioDistributionModule:
    """ API client for the On-Q Audio Distribution Module """

    NUVO_AUDIO_DIST_FQDN = 'ADM1.local' # The ADM's IP address is discovered with a mDNS query
    NUVO_AUDIO_DIST_PORT = 2112 # The ADM API listens on TCP/2112
    NUVO_API_TERMINATOR = b'\x00' # Each request/response must be terminated with this sequence

    def __init__(self, global_source):
        self.server_ip = socket.gethostbyname(AudioDistributionModule.NUVO_AUDIO_DIST_FQDN)
        self.conn = socket.create_connection((self.server_ip,
                                              AudioDistributionModule.NUVO_AUDIO_DIST_PORT))
        self.global_source = global_source
        self.payload_id = 1

    def _request(self, **kwargs):
        payload = kwargs
        payload['ID'] = self.payload_id
        logging.debug(f'sending payload {payload}')
        self.conn.send(json.dumps(payload).encode('utf-8') + \
                       AudioDistributionModule.NUVO_API_TERMINATOR)
        self.payload_id += 1
        return self._response()

    def _response(self):
        data = b''
        while AudioDistributionModule.NUVO_API_TERMINATOR not in data:
            data += self.conn.recv(1)
        res = json.loads(data[:-1])
        logging.debug(f'received {res}')
        if res.get('Service') in ['Greeting', 'ping']: # ignore greeting and keepalive
            return self._response()
        return res

    def _set_power(self, zone_id, power_on):
        self._request(Service='SetZoneProperty', ZID=zone_id, PropertyList={'Power': power_on})

    def power_off(self, zone_id):
        """
        Power off a given zone

        Arguments:
        zone_id (str) - Target zone
        """
        self._set_power(zone_id, False)

    def list_zones(self):
        """
        List available zones in the system

        Returns:
        list - List of zone data
        """
        res = self._request(Service='ListZones')
        try:
            return res['ZoneList']
        except Exception as err:
            logging.debug(traceback.format_exc())
            logging.error(err)
        return []

    def play(self, zone_id):
        """
        Power on the specified zone and start playing at 50% volume
        """
        logging.info(f'Playing in {zone_id}')
        self._request(Service='SetZoneProperty', ZID=zone_id,
                      PropertyList={'Power': True, 'Source': self.global_source, 'Volume': 50})
