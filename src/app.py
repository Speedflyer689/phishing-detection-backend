import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from library.config import Config
from library.flask import handle_generic_exception, handle_400, handle_pydantic_validation_errors

from library.model_managers import PhishingEmailDetector, PhishingUrlDetector
from resources.modules.controller import service_factory

from pydantic import ValidationError

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
api = Api(app)

app.register_error_handler(ValidationError, handle_pydantic_validation_errors)
app.register_error_handler(400, handle_400)
app.register_error_handler(Exception, handle_generic_exception)

# Initialize models
phishing_email_detector = PhishingEmailDetector()
phishing_email_detector.load()
Config.PHISHING_EMAIL_DETECTOR = phishing_email_detector

phishing_url_detector = PhishingUrlDetector()
phishing_url_detector.load()
Config.PHISHING_URL_DETECTOR = phishing_url_detector

with app.app_context():
    # db.init_app(app)
    for path, service in service_factory.items():
        api.add_resource(service, path)

if __name__ == "__main__":
    app.run(port=5000)