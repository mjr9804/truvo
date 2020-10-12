import upnpclient

def discover_device():
    devices = upnpclient.discover(timeout=2)
    try:
        device = [device for device in devices if 'NuVo' in device.friendly_name][0]
        return device
    except IndexError:
        return None

class NuVo:
    def __init__(self):
        self.device = discover_device()
        self.api = self.device.AVTransport

    def set_stream_url(self, instance_id, url):
        print(instance_id, url)
        self.api.SetAVTransportURI(InstanceID=int(instance_id), CurrentURI=url,
                                   CurrentURIMetaData='')
