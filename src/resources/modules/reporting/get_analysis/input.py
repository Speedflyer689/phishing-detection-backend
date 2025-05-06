from typing import Optional
from pydantic import BaseModel

class GetAnalysisInput(BaseModel):
    incident_type: Optional[str] = None
