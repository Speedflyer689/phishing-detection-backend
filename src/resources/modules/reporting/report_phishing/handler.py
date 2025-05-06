from interfaces.api import APIHandler
from .compute import ReportIncidentComputer
from .input import ReportIncidentInput


class ReportIncidentHandler(APIHandler):
    @property
    def api_input(self) -> ReportIncidentInput:
        return ReportIncidentInput(**self._raw_input)

    @property
    def computer(self) -> ReportIncidentComputer:
        return ReportIncidentComputer()

    @property
    def validator(self):
        return None
