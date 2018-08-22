import json

import requests

from .errors import UnexpectedResponseException


class OnsenClient:
    def __init__(self):
        self._sesson = requests.session()

    def moive_info(self, program_name):
        from .cls import MoiveInfo
        return MoiveInfo(program_name, self._sesson)

    def shown_moives(self):
        from .cls import ShownMoives
        return ShownMoives(None, self._sesson)
