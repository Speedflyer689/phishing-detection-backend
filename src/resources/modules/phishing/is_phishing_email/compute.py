from .input import PhishingEmailInput
from library.api import APIOutput, BaseComputer


class PhishingEmailComputer(BaseComputer):
    def compute(self, api_input: PhishingEmailInput) -> APIOutput:
        
        # Static data
        # @Priya843, Fix this once you are done
        
        is_phishing = True # Calculate this value using ML
        
        data = {
            "is_phishing": is_phishing
        }
        return APIOutput.success(data=data, message="Phishing email analysed")