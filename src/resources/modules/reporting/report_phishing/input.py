from pydantic import BaseModel

class ReportIncidentInput(BaseModel):
    content: str
    incident_type: str
