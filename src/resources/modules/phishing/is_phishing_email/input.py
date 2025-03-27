from pydantic import BaseModel

class PhishingEmailInput(BaseModel):
    emailSender: str
    emailText: str