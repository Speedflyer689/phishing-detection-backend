from .input import ReportIncidentInput
from library.api import APIOutput, BaseComputer
from library.logger import LOGGER

from database.models import PhishingIncident

class ReportIncidentComputer(BaseComputer):
    def compute(self, api_input: ReportIncidentInput) -> APIOutput:
        LOGGER.info("Reporting phishing incident")
        incident: PhishingIncident = PhishingIncident.query.filter(PhishingIncident.content == api_input.content, PhishingIncident.type == api_input.incident_type).first()
        
        if incident:
            incident.count += 1
            incident.save()
        else:
            incident: PhishingIncident = PhishingIncident(
                content=api_input.content,
                type=api_input.incident_type
            ).save()
        data = incident.to_dict()
        LOGGER.info(f"Output: {data}")
        return APIOutput.success(data=data, message="Phishing url stored")