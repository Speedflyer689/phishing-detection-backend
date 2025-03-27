from pydantic import BaseModel

class PhishingUrlInput(BaseModel):
    title: str
    url: str
