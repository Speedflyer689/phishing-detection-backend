from typing import Dict, Type

from flask_restful import Resource

from .is_phishing_email import PhishingEmailService
from .is_phishing_url import PhishingUrlService

phishing_factory: Dict[str, Type[Resource]] = {
    "/v1/phishing/email/detect": PhishingEmailService,
    "/v1/phishing/url/detect": PhishingUrlService,
}
   