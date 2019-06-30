import requests
import socket

class HTTPAdapterWithSocketOptions(requests.adapters.HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        super(HTTPAdapterWithSocketOptions, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super(HTTPAdapterWithSocketOptions, self).init_poolmanager(*args, **kwargs)

def getSocket():
    adapter = HTTPAdapterWithSocketOptions(socket_options=
            [
            (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ])
    s = requests.session()
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

def get(*args,**kwargs):
    s = getSocket()
    resp = s.get(*args,**kwargs)
    s.close()
    return resp

def head(*args,**kwargs):
    s = getSocket()
    resp = s.head(*args,**kwargs)
    s.close()
    return resp

def post(*args,**kwargs):
    s = getSocket()
    resp = s.post(*args,**kwargs)
    s.close()
    return resp

def options(*args,**kwargs):
    s = getSocket()
    resp = s.options(*args,**kwargs)
    s.close()
    return resp
