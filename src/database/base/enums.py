from enum import Enum

class PhishingType(str, Enum):
    URL = "URL"
    EMAIL = "EMAIL"
