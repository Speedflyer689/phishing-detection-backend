from .input import PhishingEmailInput
from library.api import APIOutput, BaseComputer
from library.config import Config
from library.logger import LOGGER

class PhishingEmailComputer(BaseComputer):
    def compute(self, api_input: PhishingEmailInput) -> APIOutput:
        LOGGER.info(f"Detecting if email is phishing or not.")
        LOGGER.info(f"Data: {api_input.model_dump()}")
        is_phishing = Config.PHISHING_EMAIL_DETECTOR.predict(api_input.emailText)
        data = {
            "is_phishing": is_phishing
        }
        LOGGER.info(f"Output: {data}")
        return APIOutput.success(data=data, message="Phishing email analysed")