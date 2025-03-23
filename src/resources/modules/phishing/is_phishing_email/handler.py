from interfaces.api import APIHandler
from .compute import PhishingEmailComputer
from .input import PhishingEmailInput


class PhishingEmailHandler(APIHandler):
    @property
    def api_input(self) -> PhishingEmailInput:
        return PhishingEmailInput(**self._raw_input)

    @property
    def computer(self) -> PhishingEmailComputer:
        return PhishingEmailComputer()

    @property
    def validator(self):
        return None
