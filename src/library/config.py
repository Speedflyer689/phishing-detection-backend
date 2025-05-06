import os
from .model_managers import PhishingEmailDetector, PhishingUrlDetector

class _DatabaseConfig:
    HOST = 'localhost'
    PORT = 5432
    NAME = os.getenv('DB_NAME', 'phishing_db')
    USER = os.getenv('DB_USER', 'postgres')
    PASSWORD = os.getenv('DB_PASSWORD', 'alphahire123')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

class _DetectorConfig:
    PHISHING_EMAIL_DETECTOR: PhishingEmailDetector
    PHISHING_URL_DETECTOR: PhishingUrlDetector

class Config():
    DB = _DatabaseConfig()
    DETECTOR = _DetectorConfig()
    pass
