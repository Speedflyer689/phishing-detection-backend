import os
from .model_managers import PhishingEmailDetector, PhishingUrlDetector

class Config:
    PHISHING_EMAIL_DETECTOR: PhishingEmailDetector
    PHISHING_URL_DETECTOR: PhishingUrlDetector