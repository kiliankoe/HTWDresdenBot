import requests
import json
from .exceptions import *


class Network:
    @staticmethod
    def get(url: str, params=None, auth=None):
        req = requests.get(url, params=params, auth=auth)
        if req.status_code == 401:
            raise HTWAuthenticationException
        elif req.status_code == 400:
            raise HTWRequestException
        elif int(req.status_code / 100) == 5:
            raise HTWServerException
        elif req.status_code != 200:
            print(req.status_code)
            print(req.text)
            return HTWBaseException

        return json.loads(req.text)
