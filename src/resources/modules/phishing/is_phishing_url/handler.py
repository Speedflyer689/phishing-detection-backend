from interfaces.api import APIHandler
from .compute import PhishingUrlComputer
from .input import PhishingUrlInput


class PhishingUrlHandler(APIHandler):
    @property
    def api_input(self) -> PhishingUrlInput:
        return PhishingUrlInput(**self._raw_input)

    @property
    def computer(self) -> PhishingUrlComputer:
        return PhishingUrlComputer()

    @property
    def validator(self):
        return None
