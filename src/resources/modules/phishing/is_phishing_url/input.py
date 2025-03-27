from pydantic import BaseModel

class PhishingUrlInput(BaseModel):
    url: str
