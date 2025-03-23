import json
from flask import request
from flask_restful import Resource

from library.logger import LOGGER

from .handler import PhishingEmailHandler


class PhishingEmailService(Resource):
    def post(self) -> dict:
        LOGGER.info(f"Checking if the email is phishing or not")
        data = json.loads(request.get_data())
        output = PhishingEmailHandler(data).handle()
        return dict(output)
