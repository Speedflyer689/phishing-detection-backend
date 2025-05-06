from interfaces.api import APIHandler
from .compute import GetAnalysisComputer
from .input import GetAnalysisInput


class GetAnalysisHandler(APIHandler):
    @property
    def api_input(self) -> GetAnalysisInput:
        return GetAnalysisInput(**self._raw_input)

    @property
    def computer(self) -> GetAnalysisComputer:
        return GetAnalysisComputer()

    @property
    def validator(self):
        return None
