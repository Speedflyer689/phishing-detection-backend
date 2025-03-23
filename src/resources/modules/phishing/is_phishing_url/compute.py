from .input import PhishingUrlInput
from library.api import APIOutput, BaseComputer


class PhishingUrlComputer(BaseComputer):
    def compute(self, api_input: PhishingUrlInput) -> APIOutput:
        
        # Static data
        # @mrboombastic69, Fix this once you are done
        
        is_phishing = True # Calculate this value using ML
        
        data = {
            "is_phishing": is_phishing
        }
        return APIOutput.success(data=data, message="Phishing url analysed")