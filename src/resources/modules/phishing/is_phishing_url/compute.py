from .input import PhishingUrlInput
from library.api import APIOutput, BaseComputer
from library.logger import LOGGER
import requests

from library.config import Config

class PhishingUrlComputer(BaseComputer):
    
    @staticmethod
    def _get_html_from_url(url: str) -> str:
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except:
            return ""
    def compute(self, api_input: PhishingUrlInput) -> APIOutput:
        
        url = api_input.url
        title = api_input.title
        html = self._get_html_from_url(url)
        LOGGER.info("Checking if url is phishing or not")
        LOGGER.info(f"URL: {url}")
        LOGGER.info(f"TITLE: {title}")
        LOGGER.info(f"HTML: {html}")
        
        
        is_phishing, confidence = Config.PHISHING_URL_DETECTOR.predict(url, title, html)
        data = {
            "is_phishing": is_phishing,
            "confidence": confidence
        }
        LOGGER.info(f"Output: {data}")
        return APIOutput.success(data=data, message="Phishing url analysed")