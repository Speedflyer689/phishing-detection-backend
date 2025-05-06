from typing import List
from .input import GetAnalysisInput
from library.api import APIOutput, BaseComputer
from library.logger import LOGGER

from database.models import PhishingIncident

class GetAnalysisComputer(BaseComputer):
    def compute(self, api_input: GetAnalysisInput) -> APIOutput:
        
        LOGGER.info("Reporting phishing incident")
        if api_input.incident_type:
            incident: List[PhishingIncident] = PhishingIncident.query.filter(PhishingIncident.type == api_input.incident_type).all()
        else:
            incident: List[PhishingIncident] = PhishingIncident.query.all()
        data = PhishingIncident.serialize(incident)
        LOGGER.info(f"Output: {data}")
        return APIOutput.success(data=data, message="Phishing url fetched")