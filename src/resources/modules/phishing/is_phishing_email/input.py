from pydantic import BaseModel

class PhishingEmailInput(BaseModel):
    emailText: str